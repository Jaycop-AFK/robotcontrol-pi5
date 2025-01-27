#!/bin/bash

source /home/torrobot/robotcontrol-pi5/venv/bin/activate



run_script() {
    local script="$1"
    while true; do
        echo "Starting $script..."
        python3 "$script"
        echo "$script crashed with exit code $?; restarting in 5 seconds..."
        sleep 5
    done
}

run_script /home/torrobot/robotcontrol-pi5/sound.py &
run_script /home/torrobot/robotcontrol-pi5/speaker.py &
run_script /home/torrobot/robotcontrol-pi5/video.py &
run_script /home/torrobot/robotcontrol-pi5/control.py &

wait 
