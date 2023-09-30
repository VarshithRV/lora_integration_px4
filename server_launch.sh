#!/bin/bash
# This script is used to launch the server

python3 ~/catkin_ws/src/Drone_control-1-manual_control-master/scripts/manual_control/server_application.py lora_input
roslaunch px4_controller server.launch