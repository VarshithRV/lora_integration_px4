# disarm the drone

import rospy
from mavros_msgs.srv import CommandBool, CommandBoolRequest
from mavros_msgs.msg import State

state = State()

def statecb(msg : State):
    global state
    state = msg

def main():
    rospy.init_node("disarm")
    rospy.wait_for_service("/mavros/cmd/arming")
    rospy.Subscriber("/mavros/state",State,callback=statecb)
    rospy.wait_for_message("/mavros/state",State)
    msg = CommandBoolRequest()
    msg.value = False
    arm = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
    
    rate = rospy.Rate(20)
    time = rospy.get_time()
    
    while (state.armed) and (not rospy.is_shutdown()) and (rospy.get_time() - time < 5.0):
        try : 
            arm.call(msg)
        except rospy.ServiceException:
            rospy.logerr("disarming failed, Service exception")
    
    rospy.loginfo(f"Arm = {state.armed}")
    if state.armed:
        rospy.logerr("Disarming Failed!, check px4 logs")
    else : 
        rospy.loginfo("Disarmed")

main()
    