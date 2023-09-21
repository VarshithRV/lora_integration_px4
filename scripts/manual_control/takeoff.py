# takeoff from the local position
# uses position ctl

takeoff_altitude = 2

import rospy
from geometry_msgs.msg import  PoseStamped, TwistStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import SetMode, SetModeRequest, SetMavFrame, SetMavFrameRequest

mav_frame = SetMavFrameRequest()
mav_frame.mav_frame = 8

local_position = PoseStamped()
state = State()

def posecb(msg : PoseStamped):
    global local_position
    local_position = msg

def statecb(msg: State):
    global state
    state = msg

def main():
    time = rospy.get_time()

    rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=posecb)
    rospy.Subscriber("mavros/state",State,callback=statecb)
    pub = rospy.Publisher("/mavros/setpoint_position/local",PoseStamped,queue_size=10)
    rospy.wait_for_message("/mavros/local_position/pose",PoseStamped)
    rospy.wait_for_message("/mavros/state",State)
    pub_vel = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel",TwistStamped,queue_size=10)
    velocity_sp = TwistStamped()
    rate = rospy.Rate(20)
    
    
    
    ###################################################### uncomment this before deployment ###########################################
    # if not state.armed:
    #     rospy.logerr("Denied! Vehicle is Disarmed")
    #     exit()
    ###################################################################################################################################
    
    rospy.loginfo(f"Takeoff altitude = {takeoff_altitude}")
    rospy.loginfo("Switching to offboard in posctl")

    setpoint_position = PoseStamped()
    setpoint_position = local_position
    setpoint_position.pose.position.z += 2
    rospy.wait_for_message("/mavros/local_position/pose",PoseStamped)

    # set to offboard mode
    rospy.loginfo("Setting to offboard moode")
    
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
                rospy.loginfo(f"Mode = {state.mode}")
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
        
    
    # taking off to 2m.
    rate = rospy.Rate(20)
    error = 0.05 # 5cm
    time = rospy.get_time()
    while not rospy.is_shutdown() and local_position.pose.position.z < takeoff_altitude - error and rospy.get_time() - time < 10.0:
        pub.publish(setpoint_position)
        rate.sleep()
    
    rospy.loginfo(f"Altitude = {local_position.pose.position.z}, Takeoff altitude reached")
    rospy.loginfo(f"Time taken = {rospy.get_time()-time}")

    # velocity hold in offboard mode
    velocity_sp = TwistStamped()
    pub_vel = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel",TwistStamped,queue_size=10)
    rospy.loginfo("Velocity hold")
    while not rospy.is_shutdown():
        pub_vel.publish(velocity_sp)
        rate.sleep()

rospy.init_node("Takeoff")
main()