#!/bin/bash
set -x
# change to script folder
cd /home/raspberrypi/Documents/source/code.maxpayne.vip/Y2-T2 || exit 1

# optional: activate venv if you use one
# source /home/raspberrypi/venv/bin/activate

# run with full python path, log stdout/stderr to file
exec /usr/bin/python3 main.py >> /home/raspberrypi/Y2-T2.log 2>&1
