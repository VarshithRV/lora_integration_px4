#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from px4_controller.msg import drone

# xbox mapping : 
# axes[0] = H left
# axes[1] = V left
# axes[3] = H right
# axes[4] = V left

# def dronecb():
class joy_input:
    def __init__(self):
        self.joy_in = Joy() #will contain the joy values
        self.drone_ip = drone() #will contain the rpty values
    
    def joycb(self,msg: Joy):
        self.joy_in = msg
        self.drone_ip.thrust = self.joy_in.axes[1]
        self.drone_ip.yaw = self.joy_in.axes[0]
        self.drone_ip.roll = self.joy_in.axes[3]
        self.drone_ip.pitch = self.joy_in.axes[4]

if __name__ == "__main__":
    rospy.init_node("joy_control")
    joy = joy_input()
    cmd_vel = Twist()
    sub = rospy.Subscriber("/joy",Joy,callback = joy.joycb)
    pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped",Twist,queue_size=10)
    
    rospy.loginfo("Establishing joystick control")
    rate = rospy.Rate(20)

    while not rospy.is_shutdown():
        cmd_vel.linear.z=3*joy.drone_ip.thrust
        cmd_vel.angular.z =3*joy.drone_ip.yaw
        cmd_vel.linear.x = 3*joy.drone_ip.pitch
        cmd_vel.linear.y = 3*joy.drone_ip.roll
        pub.publish(cmd_vel)
        rate.sleep()
