# script for landing using the service provided, autoland
# hybrid script for soft landing needs to be implemented

import rospy
from mavros_msgs.srv import CommandTOL, CommandTOLRequest, CommandTOLResponse, SetMode, SetModeRequest
from mavros_msgs.msg import State
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float64

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
    rospy.wait_for_service("/mavros/cmd/land")

    if not state.armed:
        rospy.logerr("Diarmed, already landed!")
        exit()
    
    msg = CommandTOLRequest()
    takeoff = rospy.ServiceProxy("/mavros/cmd/land",CommandTOL)
    response = CommandTOLResponse()
    
    rospy.loginfo("Landing request")
    while not rospy.is_shutdown() and state.mode != "AUTO.LAND":
        try : 
            response = takeoff.call(msg)
        except rospy.ServiceException:
            rospy.loginfo("Service exception")
    if response.success :
        rospy.loginfo(f"Landing successful")
    else : 
        rospy.logerr("Landing denied, check px4 logs")

    # change to auto.loiter mode after landing
    rospy.wait_for_service("/mavros/set_mode")
    guided_disarmed = SetModeRequest()
    guided_disarmed.base_mode = SetModeRequest.MAV_MODE_GUIDED_DISARMED
    setMode = rospy.ServiceProxy("/mavros/set_mode",SetMode)
    try :
        setMode.call(guided_disarmed)
    except rospy.ServiceException:
        rospy.logerr("Mode could not be set to preflight, landing")
        exit()
    rospy.loginfo("Mode set to guided_disarmed, landing successful")
    
rospy.init_node("land")
main()