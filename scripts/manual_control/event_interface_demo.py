from multiprocessing import Process
from pynput import keyboard
import dummy_fn


current_task = None

def on_press(key):
    global current_task
    try:
        if key.char == 'q':
            if current_task is not None:
                # stop the current task
                current_task.terminate()
                current_task.join()
            current_task = Process(target=dummy_fn.task_q)
            current_task.start()

        elif key.char == 'e':
            if current_task is not None:
                # stop the current task
                current_task.terminate()
                current_task.join()
            current_task = Process(target=dummy_fn.task_e)
            current_task.start()

        elif key.char == 'c':
            if current_task is not None:
                # stop the current task
                current_task.terminate()
                current_task.join()
            current_task = Process(target=dummy_fn.task_c)
            current_task.start()

        elif key.char == 'x':
            if current_task is not None:
                # stop the current task
                current_task.terminate()
                current_task.join()
            current_task = Process(target=dummy_fn.task_x)
            current_task.start()

        elif key.char == 'x':
            if current_task is not None:
                # stop the current task
                current_task.terminate()
                current_task.join()
            current_task = Process(target=dummy_fn.task_z)
            current_task.start()
    except AttributeError:
        pass

# Collect events until released
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()