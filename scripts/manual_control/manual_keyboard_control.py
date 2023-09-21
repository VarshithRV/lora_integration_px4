## Velocity keyboard control 

# check if the teleop node is running, if not running, then start it first or exit
# check if its armed and takeoff, check the flight mode of the copter, we need to rewrite a lot of shit again.

# node for velocity keyboard control

import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.srv import CommandBoolRequest, SetModeRequest, SetMavFrameRequest, CommandBool, SetMode, SetMavFrame
from mavros_msgs.msg import State
from px4_controller.msg import key
from geometry_msgs.msg import TwistStamped
import numpy as np
import threading

local_position = PoseStamped
keyboard_input = key()
velocity_vector = np.zeros((4,))
mav_frame = SetMavFrameRequest()
mav_frame.mav_frame = 8
state = State()
kill_sig = 0

def dead_zone_cover():
    hold_vel = TwistStamped()
    pub_vel = rospy.Publisher("/mavros/local_position/cmd_vel",TwistStamped,queue_size=10)
    rate = rospy.Rate(20)
    # publish the hold_vel
    while not rospy.is_shutdown():
        if kill_sig:
            break
        else:
            pub_vel.publish(hold_vel)
        rate.sleep()

def keycb(msg: key):
    global keyboard_input
    global velocity_vector
    keyboard_input = msg
    velocity_vector[0] = (keyboard_input.w - keyboard_input.s )
    velocity_vector[1] = (keyboard_input.a - keyboard_input.d )
    velocity_vector[2] = (keyboard_input.key_left_shift - keyboard_input.key_left_ctrl )
    velocity_vector[3] = keyboard_input.key_left - keyboard_input.key_right

def posecb(msg: PoseStamped):
    global local_position
    local_position = msg

def statecb(msg : State):
    global state
    state = msg

def check_keyboard():
    # check the frequency of the topic /keyboard
    # if the frequency is less than 2 hz, then prompt error
    global keyboard_input
    key_temp = keyboard_input
    rate = rospy.Rate(0.3)
    rospy.wait_for_message("/keyboard",key)
    while not rospy.is_shutdown():
        if (key.header.stamp.to_sec - keyboard_input.header.stamp.to_sec()) > 0.5:
            rospy.logwarn("Keyboard input frequency is less than 2 hz")
        rate.sleep()

def main():

    #### Deadzone start
    
    ### Deadzone cover
    global kill_sig
    kill_sig = 0
    dead_zone_thread = threading.Thread(target=dead_zone_cover,daemon=True)
    dead_zone_thread.start()

    sub=rospy.Subscriber("/keyboard",key,callback=keycb)
    # check_keyboard_thread = threading.Thread(target=check_keyboard,daemon=True)
    # check_keyboard_thread.start()
    sub2 = rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=posecb)
    sub_state = rospy.Subscriber("/mavros/state",State,callback=statecb)
    pub_vel = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel",TwistStamped,queue_size=10)
    rospy.wait_for_message("/mavros/state",State)

    velocity_sp = TwistStamped()
    rate = rospy.Rate(20)

#################################################################################### uncomment this before deployment ####################################
    # if not state.armed:
    #     rospy.logerr("UnArmed! control denied")
    #     exit()
##########################################################################################################################################################
    
    # set to offboard mode if not already
    if not state.armed or state.mode != "OFFBOARD":
        if state.mode != "OFFBOARD":
            rospy.logerr("Vehicle mode is not OFFBOARD")
            # set to offboard mode
            for i in range(50):
                pub_vel.publish(velocity_sp)
                rate.sleep()
            rospy.wait_for_service("/mavros/set_mode")
            offb = SetModeRequest()
            offb.custom_mode = "OFFBOARD"
            set_mode = rospy.ServiceProxy("/mavros/set_mode",SetMode)
            try : 
                set_mode.call(offb)
            except rospy.ServiceException:
                rospy.logerr("Mode could not be set to offboard, landing")
                exit()
    
    
    # set frame to body frame if not already
    frame = rospy.get_param("/mavros/setpoint_velocity/mav_frame")
    if frame != "BODY_NED":
        rospy.logwarn("Frame is not BODY_NED")
        body_frame = SetMavFrameRequest()
        body_frame.mav_frame = SetMavFrameRequest.FRAME_BODY_NED
        rospy.wait_for_service("/mavros/setpoint_velocity/mav_frame")
        set_body = rospy.ServiceProxy("/mavros/setpoint_velocity/mav_frame",SetMavFrame)
        try : 
            set_body.call(body_frame)
        except rospy.ServiceException:
            rospy.logerr("Frame not set to body NED")
            exit()

    kill_sig = 1
    dead_zone_thread.join()

    ##### Deadzone end, publishing velocity

    pub_vel = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel",TwistStamped,queue_size=10)
    velocity_sp = TwistStamped()
    rospy.loginfo("Start velocity control using keyboard")
    while not rospy.is_shutdown():
        try:
            velocity_sp.twist.linear.x = velocity_vector[0]
            velocity_sp.twist.linear.y = velocity_vector[1]
            velocity_sp.twist.linear.z = velocity_vector[2]
            velocity_sp.twist.angular.z = velocity_vector[3]
            pub_vel.publish(velocity_sp)
            rate.sleep()
        except KeyboardInterrupt:
            mav_frame.mav_frame = 1
            # set frame to body frame
            rospy.loginfo("Keyboard interrupt detected, going back to local NED frame")
            rospy.wait_for_service("/mavros/setpoint_velocity/mav_frame")
            body_frame = rospy.ServiceProxy("/mavros/setpoint_velocity/mav_frame",SetMavFrame)
            try : 
                body_frame.call(mav_frame)
            except rospy.ServiceException:
                rospy.loginfo("Body frame denied.")

rospy.init_node("manual_keyboard_control")
main()