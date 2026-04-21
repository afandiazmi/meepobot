Ah, that is a massive clue! Because it worked perfectly *before* you set up the auto-start, we can completely throw out the "NoIR camera" theory from earlier. **Your hardware is perfectly fine!**

What you are experiencing is a classic software bug called a **Race Condition** with the camera's Automatic White Balance (AWB). 

Here is exactly what is happening: When the Raspberry Pi boots up, your new systemd service launches the MEEPOBOT app as fast as humanly possible. The camera turns on and instantly starts streaming before its "eyes have adjusted" to the lighting in the room. Because it hasn't had a second to calculate the correct colors (White Balance), it panics, guesses wrong, and locks the video feed into a permanent purple/blue tint. 

When you ran it manually, the Pi had already been awake for a while, giving the camera drivers plenty of time to settle.

Here are two ways to fix this. Let's start with the easiest one!

---

### Fix 1: Add a "Snooze Button" to your Auto-Start (Recommended)

We can tell your Raspberry Pi to wait 10 seconds after booting before it launches the robot app. This gives the camera drivers and lighting sensors time to wake up and stabilize.

**Step 1:** Open your systemd service file again by typing this into your SSH terminal:
```bash
sudo nano /etc/systemd/system/meepobot.service
```

**Step 2:** Look for the `[Service]` section. We are going to add one new line: `ExecStartPre=/bin/sleep 10`. Make your file look exactly like this:

```ini
[Unit]
Description=MEEPOBOT Web Control Service
After=network.target

[Service]
Type=simple
User=robot
WorkingDirectory=/home/robot/meepobot
Environment="PATH=/home/robot/meepobot/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStartPre=/bin/sleep 10
ExecStart=/home/robot/meepobot/venv/bin/python3 /home/robot/meepobot/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Step 3:** Save and exit:
* Press `Ctrl` + `O` then `Enter` (to save).
* Press `Ctrl` + `X` (to exit).

**Step 4:** Reload the system and restart the Pi to test it:
```bash
sudo systemctl daemon-reload
sudo reboot
```
Wait about 60 seconds, then check the web page. The colors should be back to normal!

---

### Fix 2: Add a Warm-up Delay in your Python Code

If Fix 1 doesn't completely solve it, it means the camera specifically needs time *while the app is running* to adjust its colors before it starts streaming to the web page. 

You will need to edit your `app.py` file to give the camera a 2-second warm-up. 

**Step 1:** Open your app code:
```bash
nano /home/robot/meepobot/app.py
```

**Step 2:** Find where the camera is initialized in the code. Look for lines that mention `Picamera2` or `camera.start()`. You want to import the `time` module at the top of your script, and add a sleep command right after the camera starts, like this:

```python
import time

# ... (other code) ...

# Wherever your code starts the camera:
camera.start()
time.sleep(2) # <-- ADD THIS LINE! This gives the camera 2 seconds to fix its colors!
```

**Step 3:** Save (`Ctrl` + `O`, `Enter`) and exit (`Ctrl` + `X`).
**Step 4:** Restart your robot app to apply the changes:
```bash
sudo systemctl restart meepobot.service
```
