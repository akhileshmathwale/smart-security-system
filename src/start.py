import time

from src.core import setup, Recognize
from src.entry import FingerEntry
from src.constant import COMM_MOTION_DETECTED, COMM_FACE_DETECTED
from multiprocessing import Pipe, Process


sender, receiver = Pipe(duplex=True)

print("Booting up.....")
motion_process = Process(target=setup, args=(sender,))
motion_process.start()  # motion sensor is ready

# image recognizer
recognizer = Recognize()
recognizer_process = Process(target=recognizer.recognize, args=(sender, ))

# test
# recognizer_process.start()

# finger matching object
finger = FingerEntry()
finger.initialize()  # looks for the sensor [comment if not connected]

stop = False
while True:
    data = receiver.recv()
    if data == COMM_MOTION_DETECTED and not stop:
        stop = True

        # starting the face recognizer
        recognizer_process.start()
        
        # finger scan
        if finger.match_finger():
            print("[FINGER] Friendly Detected...")
        else:
            print("[FINGER] Intruder Detected...")

        time.sleep(60)  # delay for next response
        stop = False  # waiting for new response

    if data == COMM_FACE_DETECTED:
        print("[FACE] Friendly Detected...")

        # ending the recognizer process
        recognizer_process.terminate()
        recognizer.stop()

        time.sleep(60)  # delay for next reponse
        stop = False  # waiting for new response
