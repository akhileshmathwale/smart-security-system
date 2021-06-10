from time import sleep
import RPi.GPIO as GPIO

from ..constant import (MS_IN_PIN, MS_DELAY, COMM_MOTION_DETECTED)
COMM = None


def on_detect_motion(sender):
    print("Motion detected")
    sender.send(COMM_MOTION_DETECTED)


def setup(comm):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MS_IN_PIN, GPIO.IN)  # PIR

    try:
        print("Waiting for motion...")
        sleep(2)  # to stabilize sensor
        GPIO.add_event_detect(MS_IN_PIN, GPIO.RISING, callback=lambda x : on_detect_motion(comm))
        while True:
            sleep(MS_DELAY)
    except:
        print("Error in motion sensor")
        GPIO.cleanup()


def cleanup():
    GPIO.cleanup()
