# 🤖 MEEPOBOT - Web Control Interface

A Flask-based web application for controlling the MEEPOBOT on Raspberry Pi 5. Features include manual control, visual programming with Blockly, autonomous face tracking, and color line following.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-green)
![Raspberry%20Pi](https://img.shields.io/badge/Raspberry%20Pi-5-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

### 🎮 Manual Drive Remote

- **D-Pad Controls**: Forward, backward, left, right movement
- **Camera Control**: Pan (left/right) and tilt (up/down) servo control
- **Real-time Video**: Live camera feed with 320x240 resolution

### 🧩 Sequential Programming (Blockly)

- **Visual Programming**: Drag-and-drop blocks for robot movement
- **Custom Blocks**: Forward, backward, turn left, turn right, stop
- **Code Generation**: Automatic conversion to robot commands
- **Kid-Friendly**: Perfect for learning programming (ages 7+)

### 👤 Face Tracking

- **Smart Detection**: OpenCV Haar Cascade face detection
- **Proportional Control**: Smooth tracking with 3-zone control system
- **Auto-Follow**: Robot turns and moves toward detected faces
- **Adaptive Speed**: Slows down when centered, speeds up when far

### 🛣️ Line Following

- **Dynamic Color Selection**: Follow black, white, red, blue, green, yellow, or orange lines
- **HSV Color Detection**: Robust color tracking in various lighting
- **Junction Handling**: Automatically detects and navigates intersections
- **Proportional Control**: Smooth line following without oscillation

---

## 🚀 Quick Start

### Prerequisites

- Raspberry Pi 5
- MicroSD Card (32GB+)
- MEEPOBOT Hardware (motors, servos, camera, sensors)
- WiFi Network

### Installation

**📖 For complete step-by-step instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**

The deployment guide includes:

- Setting up Raspberry Pi OS with SSH (no monitor needed)
- Enabling camera and I2C
- Installing all dependencies
- Configuring auto-start on boot
- Troubleshooting common issues

**Quick Install (if you already have Raspberry Pi configured):**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv git i2c-tools libcap-dev libcamera-dev python3-libcamera python3-smbus -y

# Clone repository
git clone https://github.com/afandiazmi/meepobot.git
cd meepobot

# Create virtual environment
python3 -m venv venv --system-site-packages
source venv/bin/activate

# Install Python packages
pip install Flask numpy opencv-python lgpio smbus2
pip install --upgrade --no-cache-dir picamera2 simplejpeg

# Run the app
sudo env "PATH=$PATH" python3 app.py
```

Access the interface at: `http://YOUR_PI_IP:5000`

---

## 📂 Project Structure

```
meepobot/
├── app.py                      # Main Flask application
├── MEEPOBOT.py               # Robot hardware control library
├── DEPLOYMENT_GUIDE.md        # Complete setup instructions
├── BLOCKLY_UPDATE.md          # Blockly v12 update notes
├── README.md                  # This file
├── templates/
│   └── index.html             # Web interface UI
├── static/
│   ├── blockly/               # Blockly library (v12.3.1)
│   ├── custom_blocks.js       # Custom robot blocks
│   ├── tailwind.js            # TailwindCSS
│   └── materialdesignicons.css
└── image/
    ├── haarcascade_frontalface_default.xml
    ├── haarcascade_eye.xml
    └── haarcascade_fullbody.xml
```

---

## 🎯 Usage

### 1️⃣ Manual Control

- Click the **Manual Drive Remote** tab
- Use arrow buttons to move the robot
- Use Pan/Tilt buttons to control camera angle
- Click **STOP ALL MOTION** to emergency stop

### 2️⃣ Sequential Programming

- Click the **Sequential Programming** tab
- Drag blocks from toolbox to workspace
- Set duration for each movement
- Click **Run Program** to execute

### 3️⃣ Face Tracking

- Click the **Face Tracking** tab
- Click **Start Face Tracking**
- Show your face to the camera
- Robot will automatically follow and approach

### 4️⃣ Line Following

- Click the **Line Following** tab
- Select line color (Black, Red, Blue, Green, Yellow, White, Orange)
- Click **Start Line Follow**
- Place robot on colored line track
- Robot automatically follows line and handles junctions

---

## ⚙️ Configuration

### Camera Settings

Default servo positions (startup):

- **Pan**: 70° (center-left)
- **Tilt**: 0° (level)

### Line Following Colors (HSV Ranges)

- **Black**: Dark objects (H: 0-180, S: 0-255, V: 0-60)
- **White**: Light objects (H: 0-180, S: 0-30, V: 200-255)
- **Red**: H: 0-10 & 170-180, S: 120-255, V: 70-255
- **Blue**: H: 100-130, S: 100-255, V: 50-255
- **Green**: H: 40-80, S: 50-255, V: 50-255
- **Yellow**: H: 20-40, S: 100-255, V: 100-255
- **Orange**: H: 10-25, S: 100-255, V: 100-255

### Control Parameters

- **Face Tracking Dead Zone**: ±30 pixels
- **Line Following Dead Zone**: ±40 pixels
- **Junction Detection Threshold**: 8000 pixel area
- **Camera Resolution**: 320x240 @ 30fps

---

## 🛠️ Maintenance

### Start/Stop Service

```bash
sudo systemctl start meepobot.service
sudo systemctl stop meepobot.service
sudo systemctl restart meepobot.service
```

### Check Status

```bash
sudo systemctl status meepobot.service
```

### View Logs

```bash
sudo journalctl -u meepobot.service -f
```

### Update Code

```bash
cd /home/robot/meepobot
git pull
sudo systemctl restart meepobot.service
```

---

## 🐛 Troubleshooting

### Camera Not Working

```bash
sudo raspi-config
# Enable: Interface Options → Legacy Camera
sudo reboot
```

### I2C Devices Not Detected

```bash
sudo raspi-config
# Enable: Interface Options → I2C
i2cdetect -y 1  # Check connected devices
```

### App Won't Start

```bash
# Check logs
sudo journalctl -u meepobot.service -n 50

# Test manual run
cd /home/robot/meepobot
source venv/bin/activate
sudo env "PATH=$PATH" python3 app.py
```

For more detailed troubleshooting, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#-troubleshooting-if-something-goes-wrong).

---

## 🏗️ Technical Details

### Hardware Requirements

- **Raspberry Pi 5** (4GB or 8GB RAM)
- **Picamera2** compatible camera module
- **I2C Motor Controller** (MEEPOBOT library)
- **Ultrasonic Distance Sensor** (GPIO 20, 21)
- **2x Servo Motors** (pan: channel 10, tilt: channel 9)
- **DC Motors** with H-bridge controller

### Software Stack

- **Backend**: Flask 2.x (Python web framework)
- **Computer Vision**: OpenCV 4.x with Haar Cascades
- **Camera**: Picamera2 with libcamera backend
- **GPIO Control**: lgpio, gpiozero
- **I2C Communication**: smbus2
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Visual Programming**: Blockly v12.3.1

### Control Algorithms

- **Face Tracking**: 3-zone proportional control (dead zone, gentle, aggressive)
- **Line Following**: HSV color masking with proportional error correction
- **Junction Detection**: Multi-contour analysis with path scoring

---

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete setup instructions for Raspberry Pi 5
- **[BLOCKLY_UPDATE.md](BLOCKLY_UPDATE.md)** - Blockly v12 migration notes

---

## 🤝 Contributing

This project is designed for educational purposes. Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**Afandi Azmi**

- GitHub: [@afandiazmi](https://github.com/afandiazmi)
- Repository: [meepobot](https://github.com/afandiazmi/meepobot)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **MEEPOBOT Hardware Platform** - Educational robotics kit
- **Blockly** - Google's visual programming library
- **OpenCV** - Computer vision library
- **Raspberry Pi Foundation** - Picamera2 and libcamera
- **TailwindCSS** - Utility-first CSS framework

---

## 🌟 Support

If you find this project helpful, please ⭐ star the repository!

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ for kids learning robotics and programming**
