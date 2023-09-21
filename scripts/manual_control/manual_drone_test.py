import rospy
from geometry_msgs.msg import PoseStamped
import multiprocessing
import time

local_position = PoseStamped()

def printcb():
    while not rospy.is_shutdown():
        global local_position
        print(local_position)
        time.sleep(0.5)

def subscriber():
    def posecb(msg : PoseStamped):
        print(msg)
    rospy.init_node("Test_node")
    sub = rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=posecb)
    print("In subscriber")
    rospy.wait_for_message("/mavros/local_position/pose",PoseStamped)
    print("Got message")
    rospy.spin()

if __name__ == "__main__":
    rospy.init_node("Test_node")
    p1 = multiprocessing.Process(target=subscriber)
    p1.start()
    rospy.spin()





    # pub1 = rospy.Publisher("/mavros/setpoint_position/local",PoseStamped,queue_size=10)
    # rate = rospy.Rate(20)
    # setpoint_position = PoseStamped()
    # setpoint_position = local_position
    # setpoint_position.pose.position.z += 2
    # while not rospy.is_shutdown():
    #     pub1.publish(setpoint_position)
    #     rate.sleep()