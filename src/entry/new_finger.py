<<<<<<< HEAD
import time
import board
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint

from ..constant import MIN_FINGER_PRINTS

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

import serial
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=10)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)


def handle_error(error):
    if error == adafruit_fingerprint.OK:
        print("captured")
        return True
    if error == adafruit_fingerprint.NOFINGER:
        print("waiting..")
        return False
    if error == adafruit_fingerprint.IMAGEFAIL:
        print("Imaging error")
        return False
    if error == adafruit_fingerprint.IMAGEMESS:
        print("Image too messy")
        return False
    if error == adafruit_fingerprint.FEATUREFAIL:
        print("Could not identify features")
        return False
    if error == adafruit_fingerprint.INVALIDIMAGE:
        print("Image invalid")
        return False
    if error == adafruit_fingerprint.ENROLLMISMATCH:
        print("Prints did not match")
        return False
    if error == adafruit_fingerprint.BADLOCATION:
        print("Bad storage location")
        return False
    if error == adafruit_fingerprint.FLASHERR:
        print("Flash storage error")
        return False
    else:
        print("Other error")
        return False


def add_new_finger():
    location = int(input("Enter id (1 - 127)"))
    for finger_img in range(1, MIN_FINGER_PRINTS + 1):
        print("\nPlace a finger ... ")

        while True:
            error = finger.get_image()
            if handle_error(error):
                break

        print("\nTemplating the data")
        error = finger.image_2_tz(finger_img)
        if not handle_error(error):
            return False

        print("\nRemove finger")
        while error != adafruit_fingerprint.NOFINGER:
            error = finger.get_image()

    print("\nCreating model...")
    error = finger.create_model()
    if not handle_error(error):
        print("error creating model")
        return False

    print(f"\nStoring model for {location}")
    error = finger.store_model(location=location)
    if not handle_error(error):
        print("error storing the model")
        return False

    print("\nDone")
    return True


def match_finger():
    def detect():
        print("Waiting for finger...")
        while finger.get_image() != adafruit_fingerprint.OK:
            pass
        print("Templating...")
        if finger.image_2_tz(1) != adafruit_fingerprint.OK:
            return False
        print("Searching...")
        if finger.finger_search() != adafruit_fingerprint.OK:
            return False
        return True

    if detect():
        print("Detected #", finger.finger_id, "with confidence", finger.confidence)
        return True
    else:
        print("Finger not found")
        return False


def del_finger():
    location = int(input("Enter id (1 - 127)"))
    if finger.delete_model(location=location) == adafruit_fingerprint.OK:
        print("Deleted!")
    else:
        print("Failed to delete")
=======
import adafruit_fingerprint
import board
import serial
from digitalio import DigitalInOut, Direction

from ..constant import MIN_FINGER_PRINTS

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=10)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)


def handle_error(error):
    if error == adafruit_fingerprint.OK:
        print("Image/ Template/ Model saved")
        return True
    if error == adafruit_fingerprint.NOFINGER:
        print(".", end="", flush=True)
        return False
    if error == adafruit_fingerprint.IMAGEFAIL:
        print("Imaging error")
        return False
    if error == adafruit_fingerprint.IMAGEMESS:
        print("Image too messy")
        return False
    if error == adafruit_fingerprint.FEATUREFAIL:
        print("Could not identify features")
        return False
    if error == adafruit_fingerprint.INVALIDIMAGE:
        print("Image invalid")
        return False
    if error == adafruit_fingerprint.ENROLLMISMATCH:
        print("Prints did not match")
        return False
    if error == adafruit_fingerprint.BADLOCATION:
        print("Bad storage location")
        return False
    if error == adafruit_fingerprint.FLASHERR:
        print("Flash storage error")
        return False
    else:
        print("Other error")
        return False


def add_new_finger():
    location = int(input("Enter id (1 - 127)"))
    for finger_img in range(1, MIN_FINGER_PRINTS + 1):
        print("Place a finger ... ")

        while True:
            error = finger.get_image()
            if handle_error(error):
                break

        print("Templating the data")
        error = finger.image_2_tz(finger_img)
        if not handle_error(error):
            return False

        print("Remove finger")
        while error != adafruit_fingerprint.NOFINGER:
            error = finger.get_image()

    print("Creating model...")
    error = finger.create_model()
    if not handle_error(error):
        return False

    print(f"Storing model for {location}")
    error = finger.store_model(location=location)
    if not handle_error(error):
        return False

    print("Done")
    return True


def match_finger():
    def detect():
        print("Waiting for image...")
        while finger.get_image() != adafruit_fingerprint.OK:
            pass
        print("Templating...")
        if finger.image_2_tz(1) != adafruit_fingerprint.OK:
            return False
        print("Searching...")
        if finger.finger_search() != adafruit_fingerprint.OK:
            return False
        return True

    if detect():
        print("Detected #", finger.finger_id, "with confidence", finger.confidence)
    else:
        print("Finger not found")


def del_finger():
    location = int(input("Enter id (1 - 127)"))
    if finger.delete_model(location=location) == adafruit_fingerprint.OK:
        print("Deleted!")
    else:
        print("Failed to delete")
>>>>>>> e0dc1cc6742f8fd8e94aeb9760bf5483324a06f7
