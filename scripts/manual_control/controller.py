import rospy
from multiprocessing import Process
from pynput import keyboard
import drone
import subprocess
from pynput.keyboard import Key, Listener
import subprocess
import sys
import threading
from px4_controller.msg import key

current_task = None
system = drone.Drone()
key_values = key()

key_state={
    "key_up":0,
    "key_down":0,
    "key_left":0,
    "key_right":0,
    "key_left_shift":0,
    "key_left_ctrl":0,
    "w":0,
    "a":0,
    "s":0,
    "d":0
}

def assign(pub):
    rate = rospy.Rate(20)
    while True:
        key_values.key_up=key_state["key_up"]
        key_values.key_down=key_state["key_down"]
        key_values.key_left=key_state["key_left"]
        key_values.key_right=key_state["key_right"]
        key_values.key_left_shift=key_state["key_left_shift"]
        key_values.key_left_ctrl=key_state["key_left_ctrl"]
        key_values.w=key_state['w']
        key_values.a=key_state['a']
        key_values.s=key_state['s']
        key_values.d=key_state['d']
        pub.publish(key_values)
        rate.sleep()

def on(key:Key):
    key = str(key)
    # print(key)
    if(key=="Key.esc"):
        print("Exiting")
        subprocess.run(["stty","echo"]) # password mode
        sys.exit() # to the parent thread
    if(key=="Key.up"):
        key_state["key_up"]=1
    if(key=="Key.down"):
        key_state["key_down"]=1
    if(key=="Key.left"):
        key_state["key_left"]=1
    if(key=="Key.right"):
        key_state["key_right"]=1
    if(key=="Key.shift"):
        key_state["key_left_shift"]=1
    if(key=="Key.ctrl"):
        key_state["key_left_ctrl"]=1
    if(key=="'w'"):
        key_state["w"]=1
    if(key=="'a'"):
        key_state["a"]=1
    if(key=="'s'"):
        key_state["s"]=1
    if(key=="'d'"):
        key_state["d"]=1

def off(key:Key):
    key = str(key)
    if(key=="Key.up"):
        key_state["key_up"]=0
    if(key=="Key.down"):
        key_state["key_down"]=0
    if(key=="Key.left"):
        key_state["key_left"]=0
    if(key=="Key.right"):
        key_state["key_right"]=0
    if(key=="Key.shift"):
        key_state["key_left_shift"]=0
    if(key=="Key.ctrl"):
        key_state["key_left_ctrl"]=0
    if(key=="'w'"):
        key_state["w"]=0
    if(key=="'a'"):
        key_state["a"]=0
    if(key=="'s'"):
        key_state["s"]=0
    if(key=="'d'"):
        key_state["d"]=0

def teleop_key():
    rospy.init_node("Keypub")  
    pub=rospy.Publisher("/keyboard",key,queue_size=10)
    print("Enter the key here, use ctrl c to exit,press esc to exit")
    subprocess.run(["stty","-echo"])
    listener = Listener(on_press=on,on_release=off)
    listener.start()
    thread1=threading.Thread(target=assign, args=(pub,))
    thread1.start()
    thread1.join()
    listener.join()

def on_press(key):
    global current_task
    try:
        if key.char == 'q':
            if current_task is not None:
                # stop the current task
                current_task.terminate()
                current_task.join()
            current_task = Process(target=system.arm)
            print("arming the drone")
            current_task.start()
        elif key.char == 'e':
            if current_task is not None:
                # stop the current task
                current_task.terminate()
                current_task.join()
            current_task = Process(target=system.disarm)
            print("disarming the drone")
            current_task.start()
        elif key.char == 'c':
            if current_task is not None:
                # stop the current task
                current_task.terminate()
                current_task.join()
            current_task = Process(target=system.manual_keyboard_control)
            current_task.start()
        elif key.char == 'x':
            if current_task is not None:
                # stop the current task
                current_task.terminate()
                current_task.join()
                current_task = Process(target=system.takeoff)
            current_task.start()
        elif key.char == 'z':
            if current_task is not None:
                # stop the current task
                current_task.terminate()
                current_task.join()
            current_task = Process(target=system.land)
            current_task.start()

    except AttributeError:
        pass

subprocess.run(["stty","-echo"])
teleop_key = Process(target=teleop_key)
teleop_key.start()
print("Controller ready, q->arm, e->disarm, c->manual keyboard control, x->takeoff, z->land")
print("For manual keyboard control, use w,a,s,d to move, shift to ascend, ctrl to descend, arrows to yaw")
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()