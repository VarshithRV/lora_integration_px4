# more modular code, but the teleop node is a prerequisite

import rospy
from px4_controller.msg import key
from drone import Drone
from multiprocessing import Process
from multiprocessing.connection import Listener, Client
import time, dummy_fn

key_values = key()
current_task = None
system = Drone()

def keycb(msg:key):
    global key_values
    key_values = msg

def key_sub():
    # global values contains the keys from the sub
    global key_values
    rospy.init_node("Keysub",disable_signals=True)
    rate = rospy.Rate(20)
    
    # client side
    address = ("localhost",6000)
    conn = Client(address, authkey=b'secret password')
    
    # subscribing to the topic in a different thread
    rospy.Subscriber("/keyboard",key,keycb)

    while rospy.is_shutdown() is False:
        conn.send(key_values)
        rate.sleep()

def main():

    # Starting the sub in a diff process
    # Interprocess communication to get the key values
    sub = Process(target=key_sub)
    sub.start()

    prev_value = key()
    current_value = key()
    
    print("Starting keyboard control of the drone")    
    
    # establish connection between the sub process
    address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
    listener = Listener(address, authkey=b'secret password')
    conn = listener.accept()
    print('connection accepted from', listener.last_accepted)
    current_task = None
    while not rospy.is_shutdown():
        msg = conn.recv()
        local_key_val = msg
        prev_value = current_value
        current_value = local_key_val
        if(prev_value.q==0 and current_value.q==1):
            print("Q is pressed") # perform a dummy function
            if current_task is not None:
                current_task.terminate()
                current_task.join()
            # current_task = Process(target=dummy_fn.Task,args=(1,))
            current_task = Process(target=system.arm)
            print("Arming the drone")
            current_task.start()
        if(prev_value.e==0 and current_value.e==1):
            print("E is pressed")
            if current_task is not None:
                current_task.terminate()
                current_task.join()
            # current_task = Process(target=dummy_fn.Task,args=(1,))
            current_task = Process(target=system.disarm)
            print("Disarming the drone")
            current_task.start()
        if(prev_value.c==0 and current_value.c==1):
            print("C is pressed")
            if current_task is not None:
                current_task.terminate()
                current_task.join()
            # current_task = Process(target=dummy_fn.Task,args=(0,))
            current_task = Process(target=system.manual_keyboard_control)
            print("Establishing manual keyboard control")
            current_task.start()
        if(prev_value.x==0 and current_value.x==1):
            print("X is pressed")
            if current_task is not None:
                current_task.terminate()
                current_task.join()
            # current_task = Process(target=dummy_fn.Task,args=(0,))
            current_task = Process(target=system.takeoff)
            print("Taking off")
            current_task.start()
        if(prev_value.z==0 and current_value.z==1):
            print("Z is pressed")
            if current_task is not None:
                current_task.terminate()
                current_task.join()
            # current_task = Process(target=dummy_fn.Task,args=(0,))
            current_task = Process(target=system.land)
            print("Landing")
            current_task.start()
        if(prev_value.j==0 and current_value.j==1):
            print("J is pressed")
            if current_task is not None:
                current_task.terminate()
                current_task.join()
            # current_task = Process(target=dummy_fn.Task,args=(0,))
            current_task = Process(target=system.joy_stick_control)
            print("Swtiching to joystick control")
            current_task.start()
        time.sleep(0.05)


main()