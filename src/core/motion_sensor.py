from time import sleep
import RPi.GPIO as GPIO

from ..constant import ( MS_IN_PIN, MS_OUT_PIN, MS_DELAY )

def on_detect_motion(channel):
	print("Motion detected")
	GPIO.output(MS_OUT_PIN, True)
	sleep(3)
	GPIO.output(MS_OUT_PIN, False)

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(MS_IN_PIN, GPIO.IN) #PIR
	GPIO.setup(MS_OUT_PIN, GPIO.OUT)

	try:
		sleep(2) # to stabilize sensor
		GPIO.add_event_detect(MS_IN_PIN , GPIO.RISING, callback=on_detect_motion)
		while True:
			sleep(MS_DELAY)
	except:
		GPIO.cleanup()

def cleanup():
	GPIO.cleanup()
