from time import sleep
import RPi.GPIO as GPIO

from ..constant import ( MS_IN_PIN, MS_OUT_PIN )

def on_detect_motion(channel):
	print("Motion detected")

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(MS_IN_PIN, GPIO.IN) #PIR

	try:
		sleep(2) # to stabilize sensor
		GPIO.add_event_detect(MS_IN_PIN , GPIO.RISING, callback=on_detect_motion)
		while True:
			sleep(2)
	except:
		GPIO.cleanup()

def cleanup():
	GPIO.cleanup()
