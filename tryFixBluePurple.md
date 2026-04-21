
sudo nano /etc/systemd/system/meepobot.service






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




sudo systemctl daemon-reload
sudo reboot
