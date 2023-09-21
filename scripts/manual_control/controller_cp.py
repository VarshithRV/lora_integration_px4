import rospy
from multiprocessing import Process
from pynput import keyboard
import drone, dummy_fn
import subprocess

current_task = None
system = drone.Drone()

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
print("Controller ready, q->arm, e->disarm, c->manual keyboard control, x->takeoff, z->land")
print("Before manual_control is called, run the teleop node")
print("For manual keyboard control, use w,a,s,d to move, shift to ascend, ctrl to descend, arrows to yaw")
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
