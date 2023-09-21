# node for velocity keyboard control

import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.srv import CommandBoolRequest, SetModeRequest, SetMavFrameRequest, CommandBool, SetMode, SetMavFrame
from px4_controller.msg import key
from geometry_msgs.msg import TwistStamped
import numpy as np
import signal

# subscribe to the keyboard input, publish it in velocity_setpoints, also set a body ned frame

local_position = PoseStamped
keyboard_input = key()
velocity_vector = np.zeros((4,))
mav_frame = SetMavFrameRequest()
mav_frame.mav_frame = 8

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

def main():
    rospy.init_node("keyboard_local_velocity_control")
    sub=rospy.Subscriber("/keyboard",key,callback=keycb)
    sub2 = rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=posecb)
    rate = rospy.Rate(20)

    # send velocity setpoints
    position_sp = PoseStamped()
    position_sp.pose.position.z = 2
    velocity_sp = TwistStamped()
    velocity_sp.twist.linear.z = 1
    rate = rospy.Rate(20)

    # set frame to body frame
    rospy.loginfo("Setting to body frame")
    rospy.wait_for_service("/mavros/setpoint_velocity/mav_frame")
    body_frame = rospy.ServiceProxy("/mavros/setpoint_velocity/mav_frame",SetMavFrame)
    try : 
        body_frame(mav_frame)
    except rospy.ServiceException:
        rospy.loginfo("Body frame denied.")

    rospy.loginfo("Sending initial setpoints")
    pub_pos = rospy.Publisher("/mavros/setpoint_position/local",PoseStamped, queue_size=10)
    pub_vel = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel",TwistStamped,queue_size=10)
    for i in range(100):
        pub_vel.publish(velocity_sp)
        rate.sleep()

    rospy.loginfo("Arming the drone")

    # arm the drone
    arm = CommandBoolRequest()
    arm.value = True
    rospy.wait_for_service("mavros/cmd/arming")
    Arming = rospy.ServiceProxy("mavros/cmd/arming",CommandBool)
    try : 
        truth = Arming(arm)
    except rospy.ServiceException : 
        rospy.loginfo("Arming failed")

    rospy.loginfo("Setting to offboard mode")

    # set to offboard mode
    offboard = SetModeRequest()
    offboard.custom_mode = "OFFBOARD"
    rospy.wait_for_service("/mavros/set_mode")
    offboarding = rospy.ServiceProxy("/mavros/set_mode",SetMode)
    try : 
        offboarding(offboard)
    except rospy.ServiceException:
        rospy.loginfo("Offboard mode denied")

    # lets have a position control too
    # takeoff
    rospy.loginfo("Taking off, target altitude : 2m")
    while local_position.pose.position.z <=1.95:
        pub_pos.publish(position_sp)
        rate.sleep()
    
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
                body_frame(mav_frame)
            except rospy.ServiceException:
                rospy.loginfo("Body frame denied.")
    
main()
