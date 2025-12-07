# 🤖 MEEPOBOT Deployment Guide for Raspberry Pi 5

**For Kids (10 years and below) - Step by Step! 🎓**

This guide will help you set up your MEEPOBOT on a brand new Raspberry Pi 5, even without a monitor!

---

## 📋 What You Need

Before starting, make sure you have:

- ✅ Raspberry Pi 5 (the robot's brain!)
- ✅ MicroSD Card (32GB or bigger)
- ✅ SD Card Reader (to connect SD card to your computer)
- ✅ Computer (Windows, Mac, or Linux)
- ✅ WiFi Network (with name and password)
- ✅ Power supply for Raspberry Pi
- ✅ MEEPOBOT hardware (motors, camera, sensors)

---

## 🎯 Part 1: Prepare the SD Card

### Step 1: Download Raspberry Pi Imager

1. Go to your computer
2. Open a web browser (Chrome, Edge, Firefox, etc.)
3. Visit: https://www.raspberrypi.com/software/
4. Click the **Download** button for your computer type:
   - Windows: Click "Download for Windows"
   - Mac: Click "Download for macOS"
   - Linux: Click "Download for Linux"
5. Wait for download to finish (the file is about 20-30MB)
6. Double-click the downloaded file to install
7. Follow the installation steps (click "Next" → "Next" → "Install" → "Finish")

### Step 2: Insert SD Card

1. Take your MicroSD card
2. Put it in the SD card reader
3. Plug the reader into your computer's USB port
4. Wait for computer to recognize it (you'll hear a "ding" sound!)

### Step 3: Write Raspberry Pi OS

1. Open **Raspberry Pi Imager** (the program you just installed)
2. Click **"Choose Device"** → Select **"Raspberry Pi 5"**
3. Click **"Choose OS"** → Select **"Raspberry Pi OS (64-bit)"** (the first option)
4. Click **"Choose Storage"** → Select your SD card (be careful to pick the right one!)
5. Click the **⚙️ Settings button** (gear icon in bottom right)

### Step 4: Configure Settings (IMPORTANT!)

In the settings window, fill in these details:

**General Tab:**

- ✅ Check "Set hostname" → Type: `meepobot` (or any name you like)
- ✅ Check "Set username and password"
  - Username: `robot` (or your name)
  - Password: Choose a password you can remember! (Write it down!)
- ✅ Check "Configure wireless LAN"
  - SSID: Your WiFi name (ask your parents!)
  - Password: Your WiFi password
  - Country: Select your country (e.g., MY for Malaysia)
- ✅ Check "Set locale settings"
  - Time zone: Select your timezone (e.g., Asia/Kuala_Lumpur)
  - Keyboard layout: Select your keyboard (usually "us")

**Services Tab:**

- ✅ Check "Enable SSH"
- Select "Use password authentication"

6. Click **"Save"** to save settings
7. Click **"Next"**
8. It will warn "All data will be erased" - Click **"Yes"** (this is OK!)
9. Wait for writing... this takes about 5-10 minutes ⏳
10. When it says "Write Successful!" → Click **"Continue"**
11. Remove SD card from computer

---

## 🔌 Part 2: First Boot of Raspberry Pi

### Step 5: Insert SD Card and Power Up

1. Take the SD card out of the reader
2. Put it into your Raspberry Pi 5 (the slot on the bottom)
3. Plug in the power cable to Raspberry Pi
4. Wait for Raspberry Pi to start (about 30-60 seconds)
5. The green LED light should blink (this means it's working!)

### Step 6: Find Your Raspberry Pi's IP Address

**Option A: Check Your WiFi Router**

1. Ask an adult to help
2. Open your WiFi router's admin page (usually 192.168.1.1 or 192.168.0.1)
3. Look for "Connected Devices" or "DHCP Clients"
4. Find device named "meepobot" (or the hostname you chose)
5. Write down the IP address (looks like: 192.168.1.100)

**Option B: Use IP Scanner App**

1. Download "Fing" app on your phone (free!)
2. Open the app
3. Click "Scan"
4. Look for device named "meepobot" or "Raspberry Pi"
5. Write down the IP address

**Option C: Use Command (Advanced)**

On Windows:

```cmd
ping meepobot.local
```

On Mac/Linux:

```bash
ping meepobot.local
```

---

## 💻 Part 3: Connect to Raspberry Pi (Without Monitor!)

### Step 7: Install SSH Client (Windows Only)

**Windows 10/11:** SSH is already installed! Skip to Step 8.

**Windows 7/8:** Download PuTTY:

1. Visit: https://www.putty.org/
2. Download "putty.exe"
3. Double-click to open (no installation needed!)

### Step 8: Connect via SSH

**On Windows (PowerShell):**

1. Press `Windows Key` + `X`
2. Click "Windows PowerShell" or "Terminal"
3. Type this command (replace with YOUR IP address):

```powershell
ssh robot@192.168.1.100
```

4. Press `Enter`

**On Mac/Linux (Terminal):**

1. Open Terminal app
2. Type this command (replace with YOUR IP address):

```bash
ssh robot@192.168.1.100
```

3. Press `Enter`

**First Time Connection:**

- It will ask "Are you sure you want to continue?" → Type `yes` and press Enter
- Enter your password (the one you set in Step 4)
- You won't see the password as you type - this is normal! Just type and press Enter

**Success!** You should see:

```
robot@meepobot:~ $
```

🎉 You're now inside the Raspberry Pi!

---

## ⚙️ Part 4: Configure Raspberry Pi

### Step 9: Enable Camera and I2C

Type this command:

```bash
sudo raspi-config
```

Press Enter, then:

1. Use arrow keys (↑ ↓) to select **"3 Interface Options"** → Press Enter
2. Select **"I1 Legacy Camera"** → Press Enter
3. Select **"Yes"** → Press Enter
4. Select **"Ok"** → Press Enter
5. Use arrow keys to select **"I5 I2C"** → Press Enter
6. Select **"Yes"** → Press Enter
7. Select **"Ok"** → Press Enter
8. Press the **Right Arrow** key twice to select **"Finish"**
9. When asked to reboot → Select **"Yes"**

Wait 30 seconds for Raspberry Pi to restart, then reconnect with SSH (Step 8 again).

### Step 10: Edit Camera Configuration

Type this command:

```bash
sudo nano /boot/firmware/config.txt
```

1. Use arrow keys to scroll to the bottom of the file
2. Add these lines at the very end:

```
# Camera Configuration for Raspberry Pi 5
dtoverlay=vc4-kms-v3d
camera_auto_detect=1
```

3. Press `Ctrl` + `O` to save (press Enter to confirm)
4. Press `Ctrl` + `X` to exit
5. Reboot again:

```bash
sudo reboot
```

Wait 30 seconds, then reconnect with SSH.

---

## 📦 Part 5: Install Required Software

### Step 11: Update System

Type these commands one by one (press Enter after each):

```bash
sudo apt update
```

⏳ Wait... (about 1-2 minutes)

```bash
sudo apt upgrade -y
```

⏳ Wait... (about 5-10 minutes) - Go get a snack! 🍪

### Step 12: Install Required Packages

Copy and paste this BIG command (all one line!):

```bash
sudo apt install python3-pip python3-venv git i2c-tools libcap-dev libcamera-dev python3-libcamera python3-smbus -y
```

⏳ Wait... (about 2-3 minutes)

### Step 13: Enable pigpiod Service (for GPIO control)

Type these commands:

```bash
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

Check if it's working:

```bash
sudo systemctl status pigpiod
```

You should see green text "active (running)". Press `q` to quit.

---

## 🚀 Part 6: Download and Install Robot Code

### Step 14: Clone the Repository

Type this command:

```bash
git clone https://github.com/afandiazmi/meepobot.git
```

Move into the folder:

```bash
cd meepobot
```

### Step 15: Create Python Virtual Environment

Type these commands:

```bash
python3 -m venv venv --system-site-packages
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

You should now see `(venv)` at the start of your command line!

### Step 16: Install Python Packages

Type these commands (this might take 5-10 minutes):

```bash
pip install Flask numpy opencv-python lgpio smbus2
```

⏳ Wait...

```bash
pip install --upgrade --no-cache-dir picamera2 simplejpeg
```

⏳ Wait...

### Step 17: Test the Installation

Let's check if I2C devices are detected:

```bash
i2cdetect -y 1
```

You should see a grid with numbers (these are your connected devices).

---

## 🎮 Part 7: Run the Robot App

### Step 18: Test Manual Run

First, let's test if everything works:

```bash
sudo env "PATH=$PATH" /home/robot/meepobot/venv/bin/python3 app.py
```

**Note:** Replace `robot` with your username if different!

You should see:

```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.100:5000
```

🎉 **Success!**

### Step 19: Test from Your Computer

1. Open a web browser on your computer
2. Type in the address bar: `http://192.168.1.100:5000` (use YOUR Raspberry Pi's IP!)
3. Press Enter
4. You should see the MEEPOBOT control interface! 🤖

To stop the app:

- Press `Ctrl` + `C` in the SSH terminal

---

## 🔄 Part 8: Make App Run Automatically on Startup

### Step 20: Create System Service

Type this command:

```bash
sudo nano /etc/systemd/system/meepobot.service
```

Paste this text (copy EXACTLY):

```ini
[Unit]
Description=MEEPOBOT Web Control Service
After=network.target pigpiod.service

[Service]
Type=simple
User=root
WorkingDirectory=/home/robot/meepobot
Environment="PATH=/home/robot/meepobot/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/home/robot/meepobot/venv/bin/python3 /home/robot/meepobot/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**⚠️ IMPORTANT:** If your username is NOT "robot", change all `/home/robot/` to `/home/YOURUSERNAME/`

Save and exit:

- Press `Ctrl` + `O` → Enter (save)
- Press `Ctrl` + `X` (exit)

### Step 21: Enable Auto-Start

Type these commands:

```bash
sudo systemctl daemon-reload
sudo systemctl enable meepobot.service
sudo systemctl start meepobot.service
```

Check if it's running:

```bash
sudo systemctl status meepobot.service
```

You should see green "active (running)". Press `q` to quit.

### Step 22: Test Auto-Start

Reboot the Raspberry Pi:

```bash
sudo reboot
```

Wait 60 seconds (the robot app needs time to start).

Open your web browser and go to: `http://192.168.1.100:5000`

✨ **Magic!** The robot interface should load automatically!

---

## 🛠️ Part 9: Common Commands (For Later Use)

### How to Connect Again (SSH)

```bash
ssh robot@192.168.1.100
```

(Use your username and IP address)

### How to Stop the Robot App

```bash
sudo systemctl stop meepobot.service
```

### How to Start the Robot App

```bash
sudo systemctl start meepobot.service
```

### How to Restart the Robot App

```bash
sudo systemctl restart meepobot.service
```

### How to Check if App is Running

```bash
sudo systemctl status meepobot.service
```

Press `q` to quit the status view.

### How to View Error Logs

```bash
sudo journalctl -u meepobot.service -f
```

This shows real-time logs. Press `Ctrl` + `C` to stop viewing.

### How to Update Robot Code

```bash
cd /home/robot/meepobot
git pull
sudo systemctl restart meepobot.service
```

### How to Run App Manually (For Testing)

```bash
cd /home/robot/meepobot
source venv/bin/activate
sudo env "PATH=$PATH" python3 app.py
```

Press `Ctrl` + `C` to stop.

### How to Find Your IP Address

```bash
hostname -I
```

The first number shown is your IP address!

---

## 🐛 Troubleshooting (If Something Goes Wrong)

### Problem: Can't Connect to WiFi

**Solution:**

```bash
sudo nmcli radio wifi on
sudo nmcli device wifi rescan
sudo nmcli device wifi list
sudo nmcli device wifi connect "YourWiFiName" password "YourPassword"
```

Replace `YourWiFiName` and `YourPassword` with your actual WiFi details!

### Problem: Camera Not Working

**Solution 1:** Check camera is enabled:

```bash
sudo raspi-config
```

Go to "Interface Options" → "Legacy Camera" → Enable

**Solution 2:** Reboot:

```bash
sudo reboot
```

### Problem: I2C Devices Not Found

**Solution:**

```bash
sudo raspi-config
```

Go to "Interface Options" → "I2C" → Enable

Then:

```bash
sudo reboot
```

### Problem: App Shows Error When Starting

**Check logs:**

```bash
sudo journalctl -u meepobot.service -n 50
```

Look for red error messages. Common fixes:

**Error: "Permission denied"**

```bash
sudo chmod +x /home/robot/meepobot/app.py
```

**Error: "Module not found"**

```bash
cd /home/robot/meepobot
source venv/bin/activate
pip install Flask numpy opencv-python picamera2 lgpio smbus2 simplejpeg
```

### Problem: Web Page Won't Load

**Check if app is running:**

```bash
sudo systemctl status meepobot.service
```

**Check your IP address:**

```bash
hostname -I
```

Make sure you're using the correct IP address in your browser!

### Problem: Forgot Password

You'll need to:

1. Take out SD card
2. Put it in your computer
3. Create a file named `userconf.txt` in the boot folder
4. Content: `robot:YourPassword` (without quotes)
5. Put SD card back in Raspberry Pi
6. Boot and try again

---

## 🎓 Understanding What You Did

**Raspberry Pi Imager:** Like installing Windows/Mac on a computer, but for Raspberry Pi!

**SSH:** A way to control Raspberry Pi from another computer using text commands. No monitor needed!

**sudo:** "Super User DO" - gives you admin/teacher powers to make important changes.

**apt:** The Raspberry Pi app store manager. Installs system programs.

**pip:** The Python package manager. Installs Python libraries for your code.

**venv:** Virtual Environment - keeps your robot's Python packages separate from the system.

**systemd service:** Makes your robot app start automatically when Raspberry Pi boots up, like apps on your phone!

**I2C:** A way for Raspberry Pi to talk to sensors and motors.

**GPIO:** "General Purpose Input/Output" - the pins on Raspberry Pi that connect to motors, LEDs, sensors.

---

## 🏆 You Did It!

Congratulations! 🎉 You've successfully:

- ✅ Installed Raspberry Pi OS
- ✅ Connected without a monitor (headless setup)
- ✅ Enabled camera and sensors
- ✅ Installed Python and all libraries
- ✅ Downloaded the robot code
- ✅ Made the robot start automatically
- ✅ Learned how to control your robot remotely!

**Now you can:**

- Control your robot from any device on the same WiFi
- The robot starts automatically when you plug it in
- Update the code anytime using `git pull`

---

## 📞 Need Help?

If you get stuck:

1. Read the error message carefully
2. Check the "Troubleshooting" section above
3. Ask a teacher or parent for help
4. Search the error message on Google

Remember: Every programmer gets errors! It's part of learning. Keep trying! 💪

---

## 🌟 Next Steps

Once your robot is working:

- Try the **Manual Drive** mode to move the robot
- Use **Sequential Programming** with Blockly to create programs
- Test **Face Tracking** mode (robot follows your face!)
- Try **Line Following** mode with colored tape

**Have fun building and coding!** 🤖✨

---

_Last Updated: December 7, 2025_  
_Version: 1.0_  
_For: MEEPOBOT on Raspberry Pi 5_
