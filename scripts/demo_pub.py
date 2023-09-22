import rospy
from std_msgs.msg import String
from px4_controller.msg import key 

if __name__ == "__main__":
    rospy.init_node("demo_pub_node")
    pub = rospy.Publisher("demo_topic1", key, queue_size=10)
    rate = rospy.Rate(10)
    keyboard_ip=key()
    keyboard_ip.w=0
    keyboard_ip.a=1
    keyboard_ip.s=2
    keyboard_ip.d=3
    while not rospy.is_shutdown():
        pub.publish(keyboard_ip)
        rate.sleep()