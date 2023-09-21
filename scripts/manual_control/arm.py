# arm the drone

import rospy
from mavros_msgs.srv import CommandBool, CommandBoolRequest
from mavros_msgs.msg import State
from geometry_msgs.msg import TwistStamped
import threading

state = State()
kill_sig = 0

def statecb(msg : State):
    global state
    state = msg

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

def main():
    
    ### Deadzone start
    global kill_sig
    kill_sig = 0
    dead_zone_thread = threading.Thread(target=dead_zone_cover,daemon=True)
    dead_zone_thread.start()
    
    rospy.wait_for_service("/mavros/cmd/arming")
    rospy.wait_for_message("/mavros/state",State)
    rospy.Subscriber("/mavros/state",State,callback=statecb)
    
    msg = CommandBoolRequest()
    msg.value = True
    arm = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
    rate = rospy.Rate(20)
    time = rospy.get_time()

    while (not state.armed) and (not rospy.is_shutdown()) and (rospy.get_time() - time < 5.0):
        try : 
            arm.call(msg)
        except rospy.ServiceException:
            rospy.logerr("Arming failed, Service exception")

    rospy.loginfo(f"Arming_status = {state.armed}")
    
    if not state.armed:
        rospy.logerr("Arming Failed!, check px4 logs")
    else : 
        rospy.loginfo("Armed and ready")

    ### Deadzone end reap the thread
    kill_sig = 1

rospy.init_node("arm")
main()
    