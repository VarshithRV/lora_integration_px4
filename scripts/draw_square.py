# vx = 2, wz = 0.5
import rospy
from mavros_msgs.srv import SetMavFrame, SetMavFrameRequest
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest
from geometry_msgs.msg import PoseStamped, TwistStamped

local_position = PoseStamped()

def posecb(msg: PoseStamped):
    global local_position
    local_position = msg


if __name__=="__main__":
    rospy.init_node('Draw_circle')
    
    rospy.Subscriber('/mavros/local_position/pose', PoseStamped, posecb)
    rospy.wait_for_service('/mavros/setpoint_velocity/mav_frame')
    rospy.wait_for_message('/mavros/local_position/pose', PoseStamped)
    rospy.wait_for_service('/mavros/setpoint_position/mav_frame')

    rospy.loginfo("Node Initialized")
    
    # set velocity frame to body frame    
    mav_frame = SetMavFrameRequest()
    mav_frame.mav_frame = 8
    mav_frameService_vel = rospy.ServiceProxy('/mavros/setpoint_velocity/mav_frame', SetMavFrame)
    mav_frameService_pos = rospy.ServiceProxy('/mavros/setpoint_position/mav_frame', SetMavFrame)
    try :
        mav_frameService_vel.call(mav_frame)
    except rospy.ServiceException as e : 
        rospy.loginfo("Service mav_frame call failed %s " %e)
    # set position as local frame
    mav_frame.mav_frame = 1
    try :
        mav_frameService_pos.call(mav_frame)
    except rospy.ServiceException as e : 
        rospy.loginfo("Service mav_frame call failed %s " %e)
    rospy.loginfo("Velocity frame set to body and position to local")

    cmd_vel = TwistStamped()
    cmd_vel.twist.linear.x = 2
    cmd_vel.twist.angular.z = 0.5
    takeoff = local_position
    takeoff.pose.position.z = 5
    pub_velocity = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel",TwistStamped,queue_size=10)
    pub_position = rospy.Publisher("/mavros/setpoint_position/local",PoseStamped,queue_size=10)
    rate = rospy.Rate(20)

    rospy.loginfo("Setting to offboard mode")
    # send a few setpoints before starting
    for i in range(100):
        pub_velocity.publish(cmd_vel)
        rate.sleep()

    # set to offboardmode
    mode = SetModeRequest()
    mode.custom_mode = "OFFBOARD"
    rospy.wait_for_service('/mavros/set_mode')
    modeService = rospy.ServiceProxy('/mavros/set_mode', SetMode)
    try :
        modeService.call(mode)
    except rospy.ServiceException as e:
        rospy.loginfo("Service mode call failed %s " %e)
    rospy.loginfo("Set to Offboard mode")

    # arm the drone
    arm = CommandBoolRequest()
    arm.value = True
    rospy.wait_for_service('/mavros/cmd/arming')
    armService = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
    try : 
        armService.call(arm)
    except rospy.ServiceException as e:
        rospy.loginfo("Service arm call failed %s " %e)
    rospy.loginfo("Armed, takeoff starting")
    
    # takeoff drone to 5m
    while (not rospy.is_shutdown()) and local_position.pose.position.z < 4.5:
        pub_position.publish(takeoff)
        rate.sleep()
    rospy.loginfo("Takeoff complete, Orbit starting")

    time = rospy.Time.now()
    # move drone in circle
    while (not rospy.is_shutdown()) and rospy.Time.now() - time < rospy.Duration(30):
        pub_velocity.publish(cmd_vel)
        rate.sleep()

    # land drone
    rospy.loginfo("Landing")
    time = rospy.Time.now()
    land = local_position
    while (not rospy.is_shutdown()) and rospy.Time.now() - time < rospy.Duration(5):
        pub_position.publish(land)
        rate.sleep()
    land.pose.position.z = 0
    while (not rospy.is_shutdown()) and local_position.pose.position.z > 0.5:
        pub_position.publish(land)
        rate.sleep()