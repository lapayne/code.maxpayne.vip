# Year 2 Term 2 - The great fire of London, code to make the LED's flicker

In order to make this code run correctly we needed to make it run as a service on the raspberry pi so that the fire sound would play.

The base directory used in this case was /home/raspberrypi/source and this repo cloned into it, you will need to alter directories if you clone somewhere else.

The commands required were:

1. Create a service to run at boot by creating a file: /etc/systemd/system/ledproject.service
2. edit the file and place the following in it which will have it wait for the sound service to start first before running
```
[Unit]
Description=Y2-T2 Python app (with audio readiness)
After=network-online.target sound.target
Wants=network-online.target

[Service]
User=raspberrypi
Group=raspberrypi
# allow service to access per-user pulse socket
Environment=XDG_RUNTIME_DIR=/run/user/1000
WorkingDirectory=/home/raspberrypi/Documents/source/code.maxpayne.vip/Y2-T2
ExecStart=/usr/bin/python3 /home/raspberrypi/Documents/source/code.maxpayne.vip/Y2-T2/main.py
Restart=on-failure
RestartSec=5
# optional: delay start a little to let audio udev settle
ExecStartPre=/bin/sleep 5
StandardOutput=append:/home/raspberrypi/Y2-T2.log
StandardError=append:/home/raspberrypi/Y2-T2.err

[Install]
WantedBy=multi-user.target

```

3. Run the following commands to enable and start the service, nothing will happen yet but will trigger on a reboot.

```
sudo systemctl daemon-reload
sudo systemctl enable ledproject.service
sudo reboot now
```
