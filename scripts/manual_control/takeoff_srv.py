# Alternate takeoff script that uses Autonomous takeoff service

takeoff_altitude = 2

import rospy
from mavros_msgs.srv import CommandTOL, CommandTOLRequest, CommandTOLResponse
from mavros_msgs.msg import State
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float64
import math

global_position = NavSatFix()
yaw = Float64()
state = State()

def statecb(msg : State):
    global state
    state = msg

def gpscb(msg: NavSatFix):
    global global_position
    global_position = msg

def yawcb(msg : Float64):
    global yaw
    yaw = msg


def main():
    
    rospy.Subscriber("/mavros/global_position/global",NavSatFix,callback=gpscb)    
    rospy.Subscriber("/mavros/global_position/compass_hdg",Float64,callback=yawcb)
    rospy.Subscriber("/mavros/state",State,callback=statecb)
    rospy.wait_for_message("/mavros/global_position/global",NavSatFix)
    rospy.wait_for_message("/mavros/global_position/compass_hdg",Float64)
    rospy.wait_for_message("/mavros/state",State)
    rospy.wait_for_service("/mavros/cmd/takeoff")

    if not state.armed:
        rospy.logerr("Not armed, takeoff denied!")
        exit()
    
    msg = CommandTOLRequest()
    msg.altitude = takeoff_altitude
    takeoff = rospy.ServiceProxy("/mavros/cmd/takeoff",CommandTOL)
    response = CommandTOLResponse()
    
    rospy.loginfo("Takeoff request")
    # while not rospy.is_shutdown() and state.mode != "AUTO.TAKEOFF":
    try : 
        response = takeoff.call(msg)
    except rospy.ServiceException:
        rospy.loginfo("Service exception")
    
    if response.success :
        rospy.loginfo(f"Taking off, altitude = {takeoff_altitude}")
    else : 
        rospy.logerr("Takeoff denied, check px4 logs")

    
main()
rospy.init_node("Takeoff_and_land")
    
    
    
    
    
    # ------------------------------------------------------------------------------------------------------------------------------
    
    # # set to offboard mode after taking off
    # if not state.armed or state.mode != "OFFBOARD":
    #     if not state.armed:
    #         rospy.logerr("Vehicle not armed")
    #         exit()
    #     if state.mode != "OFFBOARD":
    #         rospy.logerr("Vehicle mode is not OFFBOARD")
    #         # set to offboard mode
    #         for i in range(50):
    #             pub_vel.publish(velocity_sp)
    #             rate.sleep()
    #         rospy.wait_for_service("/mavros/set_mode")
    #         offb = SetModeRequest()
    #         offb.custom_mode = "OFFBOARD"
    #         set_mode = rospy.ServiceProxy("/mavros/set_mode",SetMode)
    #         try : 
    #             set_mode.call(offb)
    #         except rospy.ServiceException:
    #             rospy.logerr("Mode could not be set to offboard, landing")
    #             exit()
    
    
