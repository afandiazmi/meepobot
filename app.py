from flask import Flask, render_template, Response, request, jsonify
from MEEPOBOT import MEEPOBOT
import time
import cv2
import numpy as np
import threading
import sys
from gpiozero import DistanceSensor, Button
from queue import Queue
import smbus2 as smbus
import ctypes
import inspect
import libcamera
from picamera2 import Picamera2

clbrobot = None
picamera = None
HARDWARE_INITIALIZED = False
MODE = 'STOP'
INSTRUCTION_QUEUE = Queue()
PAN_ANGLE = 70
TILT_ANGLE = 0
current_frame = None
face_cascade = None

# Line following color configuration (HSV ranges)
LINE_COLOR_MODE = 'black'  # Options: 'black', 'red', 'blue', 'green', 'yellow', 'white', 'custom'
LINE_COLOR_LOWER = np.array([0, 0, 0])      # HSV lower bound
LINE_COLOR_UPPER = np.array([180, 255, 60]) # HSV upper bound for black

try:
    face_cascade = cv2.CascadeClassifier('./image/haarcascade_frontalface_default.xml')
except:
    face_cascade = None

try:
    clbrobot = MEEPOBOT()
    makerobo_sensor = DistanceSensor(echo=21, trigger=20, max_distance=3, threshold_distance=0.2)
    
    # Initialize servo positions: pan=70, tilt=0
    clbrobot.set_servo_angle(10, 70)  # Pan servo
    clbrobot.set_servo_angle(9, 0)    # Tilt servo

    picamera = Picamera2()
    config = picamera.create_preview_configuration(main={"format": 'RGB888', "size": (320, 240)}, raw={"format": "SRGGB12", "size": (1920, 1080)})
    config["transform"] = libcamera.Transform(hflip=0, vflip=1)
    picamera.configure(config)
    picamera.start()
    
    HARDWARE_INITIALIZED = True
    
except Exception as e:
    import traceback
    traceback.print_exc() 
    print(f"FATAL INIT FAILURE: {e}") 
    HARDWARE_INITIALIZED = False

app = Flask(__name__)

def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
        
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def autonomous_task():
    global MODE, PAN_ANGLE, TILT_ANGLE, current_frame, clbrobot, picamera, face_cascade

    if not HARDWARE_INITIALIZED:
        print("Autonomous task cannot run: Hardware failed to initialize.")
        return

    while True:
        try:
            frame = picamera.capture_array()
            frame = cv2.flip(frame, 1)
            frame_with_overlay = frame.copy()
        except Exception as e:
            time.sleep(0.1)
            continue
        
        if MODE == 'STOP':
            clbrobot.t_stop(0)
            current_frame = cv2.imencode('.jpg', frame_with_overlay)[1].tobytes()
            time.sleep(0.1)
            continue
            
        elif MODE == 'SEQUENTIAL':
            if not INSTRUCTION_QUEUE.empty():
                instruction, duration = INSTRUCTION_QUEUE.get()
                
                # Execute movement command (duration is handled by MEEPOBOT internally)
                if instruction == 't_up': 
                    clbrobot.t_up(50, duration)
                elif instruction == 't_down': 
                    clbrobot.t_down(50, duration)
                elif instruction == 'turnLeft': 
                    clbrobot.turnLeft(50, duration)
                elif instruction == 'turnRight': 
                    clbrobot.turnRight(50, duration)
                elif instruction == 't_stop':
                    clbrobot.t_stop(duration)
                
                # No need for time.sleep() - MEEPOBOT already waits for duration
                clbrobot.t_stop(0)
            else:
                # Queue is empty, stop robot and return to STOP mode
                clbrobot.t_stop(0)
                MODE = 'STOP'
            
            current_frame = cv2.imencode('.jpg', frame_with_overlay)[1].tobytes()

        elif MODE == 'FACE_TRACK':
            if face_cascade:
                try:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    
                    if len(faces) > 0:
                        x, y, w, h = faces[0]
                        cv2.rectangle(frame_with_overlay, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        
                        # Draw center point
                        Xcent = int(x + w / 2)
                        Ycent = int(y + h / 2)
                        cv2.circle(frame_with_overlay, (Xcent, Ycent), 5, (0, 255, 0), -1)
                        
                        # Draw crosshair
                        cv2.line(frame_with_overlay, (160, 0), (160, 240), (255, 0, 0), 1)
                        cv2.line(frame_with_overlay, (0, 120), (320, 120), (255, 0, 0), 1)
                        
                        dispW = 320
                        errorPan = Xcent - dispW / 2
                        
                        # Proportional control with dead zone
                        # Dead zone: ±30 pixels (centered enough)
                        # Far zone: >80 pixels (turn more aggressively)
                        
                        if abs(errorPan) < 30:
                            # Face is centered - move forward
                            clbrobot.t_up(30, 0.2)
                            cv2.putText(frame_with_overlay, "FORWARD", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            time.sleep(0.2)
                            
                        elif abs(errorPan) > 80:
                            # Face is far off - turn aggressively with minimal forward
                            if errorPan > 0:
                                clbrobot.turnRight(30, 0.15)
                                cv2.putText(frame_with_overlay, "TURN RIGHT++", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                            else:
                                clbrobot.turnLeft(30, 0.15)
                                cv2.putText(frame_with_overlay, "TURN LEFT++", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                            time.sleep(0.15)
                            
                        else:
                            # Face is slightly off - gentle turn while moving forward
                            turn_speed = int(abs(errorPan) * 0.3)  # Proportional: 30-24 speed range
                            if errorPan > 0:
                                clbrobot.turnRight(turn_speed, 0.12)
                                cv2.putText(frame_with_overlay, "TURN RIGHT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
                            else:
                                clbrobot.turnLeft(turn_speed, 0.12)
                                cv2.putText(frame_with_overlay, "TURN LEFT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
                            time.sleep(0.12)
                            
                    else:
                        clbrobot.t_stop(0)
                        cv2.putText(frame_with_overlay, "SEARCHING...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        time.sleep(0.1)
                        
                except Exception as e:
                    print(f"Face tracking error: {e}")
                    clbrobot.t_stop(0)
                    time.sleep(0.1)
            else:
                MODE = 'STOP'
            
            current_frame = cv2.imencode('.jpg', frame_with_overlay)[1].tobytes()

        elif MODE == 'LINE_FOLLOW':
            try:
                # Crop the lower portion of the frame (like notebook does 60:120 of 160x120)
                crop_img = frame[150:240, 0:320]  # Adjusted for 320x240 resolution
                
                # Convert to HSV for color detection
                hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
                
                # Create mask based on selected color
                mask = cv2.inRange(hsv, LINE_COLOR_LOWER, LINE_COLOR_UPPER)
                
                # Special handling for red (spans 0 and 180 in hue)
                if LINE_COLOR_MODE == 'red':
                    mask2 = cv2.inRange(hsv, np.array([170, 120, 70]), np.array([180, 255, 255]))
                    mask = cv2.bitwise_or(mask, mask2)
                
                # Clean up the mask
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                
                contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if len(contours) > 0:
                    # Junction detection: Check if multiple significant contours exist
                    large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]
                    is_junction = len(large_contours) > 1
                    
                    # Calculate total line area (junction indicator)
                    total_line_area = sum([cv2.contourArea(cnt) for cnt in contours])
                    junction_threshold = 8000  # Large area = junction/intersection
                    
                    c = max(contours, key=cv2.contourArea)
                    M = cv2.moments(c)
                    
                    if M['m00'] > 0:
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        
                        # Draw line on the cropped image showing detected line
                        cv2.line(crop_img, (cx, 0), (cx, 90), (255, 0, 0), 2)
                        cv2.circle(crop_img, (cx, cy), 5, (0, 0, 255), -1)
                        cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)
                        
                        # JUNCTION DETECTED - Slow down and decide
                        if is_junction or total_line_area > junction_threshold:
                            cv2.putText(frame_with_overlay, "JUNCTION - Deciding...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)
                            
                            # Slow down at junction
                            clbrobot.t_up(15, 0.15)
                            time.sleep(0.15)
                            
                            # Decision logic: Find the contour most aligned with forward direction
                            # Check which path is most "straight ahead" (closest to center-bottom)
                            best_contour = None
                            best_score = float('inf')
                            
                            for cnt in large_contours:
                                M_cnt = cv2.moments(cnt)
                                if M_cnt['m00'] > 0:
                                    cnt_cx = int(M_cnt['m10'] / M_cnt['m00'])
                                    cnt_cy = int(M_cnt['m01'] / M_cnt['m00'])
                                    # Score: distance from center + prefer paths lower in frame (ahead)
                                    score = abs(cnt_cx - 160) + (90 - cnt_cy) * 0.5
                                    if score < best_score:
                                        best_score = score
                                        best_contour = cnt
                            
                            # Use best path if found, otherwise use largest
                            if best_contour is not None:
                                M_best = cv2.moments(best_contour)
                                if M_best['m00'] > 0:
                                    cx = int(M_best['m10'] / M_best['m00'])
                                    # Mark chosen path
                                    cv2.drawContours(crop_img, [best_contour], -1, (255, 0, 255), 3)
                        
                        # Smooth proportional line following with wider dead zone
                        error = cx - 160  # Error from center (160px)
                        
                        if abs(error) < 40:  # Dead zone - line is centered enough
                            # Go straight when line is reasonably centered
                            speed = 25 if (is_junction or total_line_area > junction_threshold) else 35
                            clbrobot.t_up(speed, 0.15)
                            cv2.putText(frame_with_overlay, "Forward", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            time.sleep(0.15)
                            
                        elif abs(error) > 100:  # Line is far off - aggressive turn
                            turn_speed = 20
                            turn_duration = 0.08
                            if error > 0:  # Line on right
                                clbrobot.turnRight(turn_speed, turn_duration)
                                cv2.putText(frame_with_overlay, "Turn Right++", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                            else:  # Line on left
                                clbrobot.turnLeft(turn_speed, turn_duration)
                                cv2.putText(frame_with_overlay, "Turn Left++", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                            time.sleep(0.08)
                            
                        else:  # Gentle correction - proportional control
                            turn_speed = int(abs(error) * 0.15)  # Slower turns: 6-15 speed
                            turn_duration = 0.06
                            if error > 0:  # Line slightly right
                                clbrobot.turnRight(turn_speed, turn_duration)
                                cv2.putText(frame_with_overlay, "Adjust Right", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
                            else:  # Line slightly left
                                clbrobot.turnLeft(turn_speed, turn_duration)
                                cv2.putText(frame_with_overlay, "Adjust Left", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
                            time.sleep(0.06)
                    else:
                        clbrobot.t_stop(0)
                        cv2.putText(frame_with_overlay, "No line detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        time.sleep(0.1)
                else:
                    clbrobot.t_stop(0)
                    cv2.putText(frame_with_overlay, "Searching...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    time.sleep(0.1)
                
                # Put the processed crop back into frame for visualization
                frame_with_overlay[150:240, 0:320] = crop_img
                
            except Exception as e:
                print(f"Line follow error: {e}")
                clbrobot.t_stop(0)
                time.sleep(0.1)
            
            current_frame = cv2.imencode('.jpg', frame_with_overlay)[1].tobytes()

        time.sleep(0.02)  # Small delay for all modes to prevent CPU overload

t = threading.Thread(target=autonomous_task)
t.daemon = True
t.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manual_control', methods=['POST'])
def manual_control():
    global MODE
    
    command = request.json.get('command')
    speed = request.json.get('speed', 50)
    
    MODE = 'MANUAL'
    
    if clbrobot:
        if command == 'forward':
            clbrobot.t_up(speed, 0)
        elif command == 'backward':
            clbrobot.t_down(speed, 0)
        elif command == 'left':
            clbrobot.turnLeft(speed, 0)
        elif command == 'right':
            clbrobot.turnRight(speed, 0)
        elif command == 'stop':
            clbrobot.t_stop(0)
            MODE = 'STOP'
    
    return jsonify({'status': 'ok', 'command': command, 'mode': MODE})

@app.route('/servo_control', methods=['POST'])
def servo_control():
    global PAN_ANGLE, TILT_ANGLE
    
    servo = request.json.get('servo')
    action = request.json.get('action')
    step = 5
    
    if clbrobot:
        if servo == 'pan':
            if action == 'increment': PAN_ANGLE += step
            elif action == 'decrement': PAN_ANGLE -= step
            PAN_ANGLE = max(min(PAN_ANGLE, 180), 0)
            clbrobot.set_servo_angle(10, PAN_ANGLE)
            
        elif servo == 'tilt':
            if action == 'increment': TILT_ANGLE += step
            elif action == 'decrement': TILT_ANGLE -= step
            TILT_ANGLE = max(min(TILT_ANGLE, 90), 0)
            clbrobot.set_servo_angle(9, TILT_ANGLE)

    return jsonify({'status': 'ok', 'pan': PAN_ANGLE, 'tilt': TILT_ANGLE})

@app.route('/run_instructions', methods=['POST'])
def run_instructions():
    global MODE

    with INSTRUCTION_QUEUE.mutex:
        INSTRUCTION_QUEUE.queue.clear()
        
    instructions_str = request.json.get('instructions')
    
    for instruction_pair in instructions_str.split(','):
        try:
            cmd, duration = instruction_pair.split(':')
            duration = float(duration)
            if cmd in ['t_up', 't_down', 'turnLeft', 'turnRight', 't_stop']:
                INSTRUCTION_QUEUE.put((cmd, duration))
        except:
            pass

    if not INSTRUCTION_QUEUE.empty():
        MODE = 'SEQUENTIAL'
        return jsonify({'status': 'running', 'mode': MODE, 'count': INSTRUCTION_QUEUE.qsize()})
    else:
        return jsonify({'status': 'failed', 'message': 'No valid instructions parsed.'})

@app.route('/set_mode', methods=['POST'])
def set_mode():
    global MODE
    
    new_mode = request.json.get('mode')
    
    if new_mode in ['FACE_TRACK', 'LINE_FOLLOW', 'STOP']:
        MODE = new_mode
        if MODE == 'STOP' and clbrobot:
            clbrobot.t_stop(0)
            
        return jsonify({'status': 'mode_set', 'mode': MODE})
    
    return jsonify({'status': 'failed', 'message': 'Invalid mode specified.'})

@app.route('/set_line_color', methods=['POST'])
def set_line_color():
    global LINE_COLOR_MODE, LINE_COLOR_LOWER, LINE_COLOR_UPPER
    
    color = request.json.get('color', 'black')
    LINE_COLOR_MODE = color
    
    # Predefined HSV color ranges
    color_ranges = {
        'black':  ([0, 0, 0],      [180, 255, 60]),
        'white':  ([0, 0, 200],    [180, 30, 255]),
        'red':    ([0, 120, 70],   [10, 255, 255]),    # Red wraps around hue
        'red2':   ([170, 120, 70], [180, 255, 255]),   # Red second range
        'blue':   ([100, 100, 50], [130, 255, 255]),
        'green':  ([40, 50, 50],   [80, 255, 255]),
        'yellow': ([20, 100, 100], [40, 255, 255]),
        'orange': ([10, 100, 100], [25, 255, 255]),
    }
    
    if color in color_ranges:
        LINE_COLOR_LOWER = np.array(color_ranges[color][0])
        LINE_COLOR_UPPER = np.array(color_ranges[color][1])
        return jsonify({'status': 'color_set', 'color': color, 
                       'lower': LINE_COLOR_LOWER.tolist(), 
                       'upper': LINE_COLOR_UPPER.tolist()})
    
    return jsonify({'status': 'failed', 'message': 'Invalid color specified.'})

def gen_frames():
    global current_frame
    while True:
        if current_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')
        else:
            time.sleep(0.05)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def shutdown_session(exception=None):
    global clbrobot, picamera
    if clbrobot:
        clbrobot.t_stop(0)
    if picamera:
        picamera.stop()
    print("Application shutdown and robot/camera stopped.")

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)
    except KeyboardInterrupt:
        shutdown_session()