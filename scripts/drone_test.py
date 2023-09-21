import rospy

rospy.init_node("TEstNode")
x = rospy.get_param("/mavros/setpoint_velocity/mav_frame")
rospy.loginfo(f"{x}, {type(x)}")


# # import rospy
# # from mavros_msgs.msg import PositionTarget, State
# # from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest
# # from geometry_msgs.msg import PoseStamped
# # from px4_controller.msg import key

# # keyboard = key()
# # local_position = PoseStamped()
# # state = State

# # def keycb(msg: key):
# #     global keyboard
# #     keyboard = msg

# # def posecb(msg: PoseStamped):
# #     global local_position
# #     local_position = msg

# # def statecb(msg : State):
# #     global state
# #     state = msg


# # def main():
# #     rospy.init_node("Position_control")
# #     pub_raw = rospy.Publisher("/mavros/setpoint_raw/local", PositionTarget, queue_size=10)
# #     pub_position = rospy.Publisher("/mavros/setpoint_position/local", PoseStamped, queue_size=10)
# #     sub_key = rospy.Subscriber("/keyboard", key, callback=keycb)
# #     sub_pose = rospy.Subscriber("/mavros/local_position/pose", PoseStamped, callback=posecb)
# #     sub_state = rospy.Subscriber("/mavros/state",State,callback=statecb)
    
# #     rospy.loginfo("Initializing position control")
# #     position = PositionTarget()
# #     position.coordinate_frame = PositionTarget.FRAME_BODY_NED
# #     position.position.z = 2
# #     # position.type_mask = PositionTarget.IGNORE_VX | PositionTarget.IGNORE_VY | PositionTarget.IGNORE_VZ \
# #     #                                 | PositionTarget.IGNORE_AFX | PositionTarget.IGNORE_AFY | PositionTarget.IGNORE_AFZ \
# #     #                                 | PositionTarget.IGNORE_YAW_RATE

# #     # takeoff_altitude = PoseStamped()
# #     # takeoff_altitude.pose.position.z = 2

# #     # provide initial setpoints
# #     rospy.loginfo("Providing initial setpoints")
# #     rate = rospy.Rate(20)
# #     for i in range(100):
# #         pub_raw.publish(position)
# #         rate.sleep()
    
# #     # set to offboard mode
# #     rospy.loginfo("Arming status = %s, Mode = %s",str(state.armed), str(state.mode))
# #     offb = SetModeRequest()
# #     offb.custom_mode = "OFFBOARD"
# #     rospy.wait_for_service("/mavros/set_mode")
# #     offboard = rospy.ServiceProxy("/mavros/set_mode",SetMode)
# #     try : 
# #         offboard.call(offb)
# #     except rospy.ServiceException:
# #         rospy.loginfo("Not set to offboard mode, Service exception")
# #         pass
# #     rospy.loginfo("Arming status = %s, Mode = %s",str(state.armed), str(state.mode))

# #     # arm the drone
# #     rospy.loginfo("Arming the drone")
# #     arm = CommandBoolRequest()
# #     arm.value = True
# #     rospy.wait_for_service("/mavros/cmd/arming")
# #     arming = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
# #     try :
# #         arming.call(arm)
# #     except rospy.ServiceException:
# #         rospy.loginfo("Arming denied, service exception")
# #         pass
# #     rospy.loginfo("Arming status = %s, Mode = %s",str(state.armed), str(state.mode))

# #     # WE NEED TO TAKEOFF HERE
# #     while not rospy.is_shutdown():
# #         pub_raw.publish(position)
# #         rate.sleep()

# # main()














# # ----------------------------------------------------------------------------------------

# # get roatated lol, publishing to the setpoint_raw topic
# import rospy
# from mavros_msgs.msg import PositionTarget
# from geometry_msgs.msg import PoseStamped
# from std_msgs.msg import Header

# local_position = PoseStamped()

# def posecb(msg : PoseStamped):
#     local_position = msg

# def main():
#     rospy.init_node("Wee_node")
#     sub = rospy.Subscriber("/mavros/local_position/pose", PoseStamped, callback=posecb)
#     pub = rospy.Publisher("/mavros/setpoint_raw/local", PositionTarget, queue_size=10)
#     position_raw = PositionTarget()
#     position_raw.header = Header()
#     position_raw.coordinate_frame = PositionTarget.FRAME_BODY_NED
#     # position_raw.type_mask = (PositionTarget.IGNORE_AFX|PositionTarget.IGNORE_AFY|PositionTarget.IGNORE_AFZ|
#     #                           PositionTarget.IGNORE_PX|PositionTarget.IGNORE_PY|PositionTarget.IGNORE_PZ |
#     #                           PositionTarget.IGNORE_VX|PositionTarget.IGNORE_VY|PositionTarget.IGNORE_VZ|
#     #                           PositionTarget.IGNORE_YAW_RATE)
#     # position_raw.type_mask = (PositionTarget.IGNORE_AFX|PositionTarget.IGNORE_AFY|PositionTarget.IGNORE_AFZ|
#     #                           PositionTarget.IGNORE_PX|PositionTarget.IGNORE_PY|PositionTarget.IGNORE_PZ |
#     #                           PositionTarget.IGNORE_VX|PositionTarget.IGNORE_VY|PositionTarget.IGNORE_VZ|
#     #                           PositionTarget.IGNORE_YAW_RATE)
#     position_raw.yaw = 0
#     rate = rospy.Rate(20)
#     offset=0.01
#     rospy.loginfo("Publishing to the topic")
#     while not rospy.is_shutdown():
#         position_raw.yaw += offset
#         pub.publish(position_raw)
#         rate.sleep()

# main()

