# node to read the state of the drone, its velocity, location, state
import rospy
from geometry_msgs.msg import PoseStamped
from math import atan, asin, degrees, atan2

local_pose = PoseStamped()

def pose_cb(msg: PoseStamped):
    global local_pose
    local_pose = msg

def main():
    rospy.init_node("State_sub")
    rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=pose_cb)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        qw = local_pose.pose.orientation.w
        qx = local_pose.pose.orientation.x
        qy = local_pose.pose.orientation.y
        qz = local_pose.pose.orientation.z
        roll = atan2(2.0*(qy*qz + qw*qx), qw*qw - qx*qx - qy*qy + qz*qz)
        pitch = asin(-2.0*(qx*qz - qw*qy))
        yaw = atan2(2.0*(qx*qy + qw*qz), qw*qw + qx*qx - qy*qy - qz*qz)
        # rospy.loginfo("%s %s %s %s",qw,qx,qy,qz)
        rospy.loginfo("pitch : %s, yaw : %s, roll : %s", degrees(pitch), degrees(yaw), degrees(roll))
        rate.sleep()

main()