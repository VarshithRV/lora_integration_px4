#!/bin/bash
# This script is used to launch the server
roslaunch px4_controller server.launch
python3 ~/catkin_ws/src/px4_controller/scripts/manual_control/server_application.py lora_input
```