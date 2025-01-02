#!/bin/bash

source /home/torrobot/torrobot/venv/bin/activate



run_script() {
    local script="$1"
    while true; do
        echo "Starting $script..."
        python3 "$script"
        echo "$script crashed with exit code $?; restarting in 5 seconds..."
        sleep 5
    done
}

run_script /home/torrobot/torrobot/sound.py &
run_script /home/torrobot/torrobot/speaker.py &
run_script /home/torrobot/torrobot/video.py &
run_script /home/torrobot/torrobot/control.py &

wait 