import time

from src.core import setup, recognize
from src.entry import match_finger
from src.constant import COMM_MOTION_DETECTED
from multiprocessing import Pipe, Process

sender, receiver = Pipe(duplex=True)


print("Booting up.....")
p = Process(target=setup, args=(sender,))
p.start()

stop = True
while True:
    data = receiver.recv()
    if data == COMM_MOTION_DETECTED and stop:
        #recognize()
        stop = False
        
        # finger scan
        if match_finger():
            print("Friendly detected...")
        else:
            print("Intruder detected...")

        time.sleep(60)  # delay for next response
        stop = True  # waiting for new response
