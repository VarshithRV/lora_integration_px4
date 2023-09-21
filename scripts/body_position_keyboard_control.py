# node for position control in body frame, with yaw, given in degrees
# right now its classic position control, need to convert it to raw position control
import rospy
from mavros_msgs.msg import PositionTarget, State
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest, SetMavFrame, SetMavFrameRequest
from geometry_msgs.msg import PoseStamped
from px4_controller.msg import key
from std_msgs.msg import Header

keyboard = key()
local_position = PoseStamped()
state = State

def keycb(msg: key):
    global keyboard
    keyboard = msg

def posecb(msg: PoseStamped):
    global local_position
    local_position = msg

def statecb(msg : State):
    global state
    state = msg

def main():
    rospy.init_node("Position_control")
    pub_position_raw = rospy.Publisher("/mavros/setpoint_raw/local", PositionTarget, queue_size=10)
    pub_position_setpoint = rospy.Publisher("/mavros/setpoint_position/local", PoseStamped, queue_size=10)
    sub_key = rospy.Subscriber("/keyboard", key, callback=keycb)
    sub_pose = rospy.Subscriber("/mavros/local_position/pose", PoseStamped, callback=posecb)
    sub_state = rospy.Subscriber("/mavros/state",State,callback=statecb)

    # change the frame to body frame for position control setpoints
    frame = SetMavFrameRequest()
    frame.mav_frame = SetMavFrameRequest.FRAME_LOCAL_NED
    rospy.wait_for_service("/mavros/setpoint_position/mav_frame")
    body_frame = rospy.ServiceProxy("/mavros/setpoint_position/mav_frame",SetMavFrame)
    try :
        body_frame.call(frame)
    except rospy.ServiceException: 
        rospy.loginfo("Frame change to body NED denied")
    rospy.loginfo("Frame changed to BODY NED")
    
    rospy.loginfo("Initializing position control")
    position_raw = PositionTarget()
    position_raw.header = Header()
    position_raw.coordinate_frame = PositionTarget.FRAME_LOCAL_NED
    position_raw.type_mask = (PositionTarget.IGNORE_AFX|PositionTarget.IGNORE_AFY|PositionTarget.IGNORE_AFZ|
                              PositionTarget.IGNORE_PX|PositionTarget.IGNORE_PY|PositionTarget.IGNORE_PZ |
                              PositionTarget.IGNORE_VX|PositionTarget.IGNORE_VY|PositionTarget.IGNORE_VZ|
                              PositionTarget.IGNORE_YAW_RATE)
    position_raw.yaw = 0
    position_setpoint = PoseStamped()
    position_setpoint.pose.position.z = 2

    # provide initial setpoints
    rospy.loginfo("Providing initial setpoints")
    rate = rospy.Rate(20)
    for i in range(100):
        pub_position_setpoint.publish(position_setpoint)
        pub_position_raw.publish(position_raw)
        rate.sleep()
    
    # set to offboard mode
    rospy.loginfo("Arming status = %s, Mode = %s",str(state.armed), str(state.mode))
    offb = SetModeRequest()
    offb.custom_mode = "OFFBOARD"
    rospy.wait_for_service("/mavros/set_mode")
    offboard = rospy.ServiceProxy("/mavros/set_mode",SetMode)
    try : 
        offboard.call(offb)
    except rospy.ServiceException:
        rospy.loginfo("Not set to offboard mode, Service exception")
        pass
    rospy.loginfo("Arming status = %s, Mode = %s",str(state.armed), str(state.mode))

    # arm the drone
    rospy.loginfo("Arming the drone")
    arm = CommandBoolRequest()
    arm.value = True
    rospy.wait_for_service("/mavros/cmd/arming")
    arming = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
    try :
        arming.call(arm)
    except rospy.ServiceException:
        rospy.loginfo("Arming denied, service exception")
        pass
    rospy.loginfo("Arming status = %s, Mode = %s",str(state.armed), str(state.mode))
    
    # need to take off
    rospy.loginfo("Taking off to an altitude of 2m")
    while (not rospy.is_shutdown()) and local_position.pose.position.z <= 1.95:
        pub_position_setpoint.publish(position_setpoint)
        pub_position_raw.publish(position_raw)
        # pub_position_raw.publish(position_raw)
        rate.sleep()
    rospy.loginfo("Altitude  = %s",str(local_position.pose.position.z))


    # start position control
    rospy.loginfo("Start position control using keyboard")
    while not rospy.is_shutdown():

        # if keyboard.w:
        #     position.position.x += 0.1
        # if keyboard.s:
        #     position.position.x -= 0.1
        # if keyboard.a:
        #     position.position.y -= 0.1
        # if keyboard.d:
        #     position.position.y += 0.1
        # if keyboard.key_left_ctrl:
        #     position.position.z -= 0.1
        # if keyboard.key_left_shift:
        #     position.position.z += 0.1
        
        if keyboard.w:
            position_setpoint.pose.position.x += 0.1
        if keyboard.s:
            position_setpoint.pose.position.x -= 0.1
        if keyboard.a:
            position_setpoint.pose.position.y += 0.1
        if keyboard.d:
            position_setpoint.pose.position.y -= 0.1
        if keyboard.key_left_ctrl:
            position_setpoint.pose.position.z -= 0.1
        if keyboard.key_left_shift:
            position_setpoint.pose.position.z += 0.1
        
        # pub_position_raw.publish(position_raw)
        pub_position_setpoint.publish(position_setpoint)
        rate.sleep()

main()