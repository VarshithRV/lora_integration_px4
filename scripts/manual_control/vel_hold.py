# node to hold position in between the nodes
# sub to local_position/velocity_body and pub to setpoint_velocity/cmd_vel in body frame 

# node for velocity keyboard control

#-------------
# We need a handler to see what we need to do if arming status chages
# We need to switch to land while checking if something geos wrong, we need to list what might go wrong in each node
#-------------


import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.srv import  SetMavFrameRequest, SetMavFrame, SetMode, SetModeRequest
from mavros_msgs.msg import State
from geometry_msgs.msg import TwistStamped

def posecb(msg: PoseStamped):
    global local_position
    local_position = msg

def statecb(msg : State):
    global state
    state = msg

def main():
    time = rospy.get_time()
    sub_position = rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=posecb)
    sub_state = rospy.Subscriber("/mavros/state",State,callback=statecb)
    rospy.wait_for_message("/mavros/state",State)
    pub_vel = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel",TwistStamped,queue_size=10)
    rate = rospy.Rate(20)
    velocity_sp = TwistStamped()
    

    if not state.armed or state.mode != "OFFBOARD":
        if not state.armed:
            rospy.logerr("Vehicle not armed")
            exit()
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

    rospy.loginfo(f"time = {rospy.get_time() - time}")
    while not rospy.is_shutdown():
        pub_vel.publish(velocity_sp)
        rate.sleep()
    

rospy.init_node("velocity_hold")
main()
