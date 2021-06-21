import time
import RPi.GPIO as GPIO

from src.core import setup, Recognize
from src.entry import FingerEntry
from src.constant import COMM_MOTION_DETECTED, COMM_FACE_DETECTED, COMM_FINGER_DETECTED, COMM_INTRUDER_DETECTED
from multiprocessing import Pipe, Process


sender, receiver = Pipe(duplex=True)

# finger matching object
finger = FingerEntry()
finger.initialize()  # looks for the sensor [comment if not connected]

print("Booting up.....")
motion_process = Process(target=setup, args=(sender,))
motion_process.start()  # motion sensor is ready

# image recognizer
recognizer = Recognize()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

check = False
while True:
    data = receiver.recv()
    if data == COMM_MOTION_DETECTED and not check:
        check = True

        # starting the face recognizer and finger sensor
        recognizer_process = Process(target=recognizer.recognize, args=(sender, ))
        recognizer_process.start()

        try:
            finger.match_finger(sender)
        except RuntimeError:
            print("[ERROR] Sensor error occurred.")
            # data = COMM_INTRUDER_DETECTED

    if data == COMM_FACE_DETECTED and check:
        print("[FACE] Friendly Detected...")
        GPIO.setup(26,GPIO.OUT)
        print("LED ON")
        GPIO.output(26,GPIO.HIGH)
        time.sleep(5)
        print("LED OFF")
        GPIO.output(26,GPIO.LOW)
        # ending the recognizer process
        recognizer_process.terminate()
        recognizer.stop()

        check = False  # waiting for new response

    if data == COMM_FINGER_DETECTED and check:
        print("[FINGER] Friendly Detected...")
        GPIO.setup(26,GPIO.OUT)
        print("LED ON")
        GPIO.output(26,GPIO.HIGH)
        time.sleep(5)
        GPIO.output(26,GPIO.LOW)
        if recognizer_process.is_alive:
            recognizer_process.terminate()

        check = False # waiting for new reponse
        time.sleep(60)

    if data == COMM_INTRUDER_DETECTED and check:
        print("[INTRUDER] Intruder detected....")

        if recognizer_process and recognizer_process.is_alive:
            recognizer_process.terminate()

        time.sleep(60)
        check = False
