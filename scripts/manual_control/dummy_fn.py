import time
def task(flag,key):
    if flag == 0:
        while True:
            print(key.char)
            time.sleep(0.5)
    else :
        for i in range(5):
            print(key.char)
            time.sleep(0.5)

def Task(flag):
    if flag == 0:
        while True:
            print("Forever")
            time.sleep(0.5)
    else :
        for i in range(5):
            print("5 times")
            time.sleep(0.5)