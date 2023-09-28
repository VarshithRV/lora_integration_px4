# intermediate bridge between lora and ros
# Receives data from the topic /lora_messages(of type String) as a json string
# And publishes it to the topic /lora_input of type key

import rospy
import time
from std_msgs.msg import String
from px4_controller.msg import key
import json

key_input = key()

def loracb(msg:String):
    file = json.loads(msg.data)
    key_input.w = file['a']
    key_input.a = file['b']
    key_input.s = file['c']
    key_input.d = file['d']
    key_input.q = file['e']
    key_input.e = file['f']
    key_input.z = file['g']
    key_input.x = file['h']
    key_input.c = file['i']
    key_input.key_left_shift = file['j']
    key_input.key_left_ctrl = file['k']
    key_input.key_left = file['l']
    key_input.key_right = file['m']
    

if __name__ == "__main__":
    rospy.init_node("lora_bridge")
    rospy.loginfo("Node Initialized, subscribing to json file from /lora_message and publishing to /lora_input")
    pub = rospy.Publisher("/lora_input", key, queue_size=10)
    rospy.Subscriber("/lora_messages", String, loracb)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        pub.publish(key_input)
        rate.sleep()
