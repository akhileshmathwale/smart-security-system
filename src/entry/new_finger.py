import adafruit_fingerprint
import serial

from ..constant import MIN_FINGER_PRINTS

uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=10)


class FingerEntry:
    def __init__(self):
        self._finger = None

    def initialize(self):
        self._finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

    def handle_error(self, error):
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

    def add_new_finger(self):
        location = int(input("Enter id (1 - 127)"))
        for finger_img in range(1, MIN_FINGER_PRINTS + 1):
            print("Place a finger ... ")

            while True:
                error = self._finger.get_image()
                if self.handle_error(error):
                    break

            print("Templating the data")
            error = self._finger.image_2_tz(finger_img)
            if not self.handle_error(error):
                return False

            print("Remove finger")
            while error != adafruit_fingerprint.NOFINGER:
                error = self._finger.get_image()

        print("Creating model...")
        error = self._finger.create_model()
        if not self.handle_error(error):
            return False

        print(f"Storing model for {location}")
        error = self._finger.store_model(location=location)
        if not self.handle_error(error):
            return False

        print("Done")
        return True

    def match_finger(self):
        def detect():
            print("Waiting for image...")
            while self._finger.get_image() != adafruit_fingerprint.OK:
                pass
            print("Templating...")
            if self._finger.image_2_tz(1) != adafruit_fingerprint.OK:
                return False
            print("Searching...")
            if self._finger.finger_search() != adafruit_fingerprint.OK:
                return False
            return True

        if detect():
            print("Detected #", self._finger.finger_id, "with confidence", self._finger.confidence)
        else:
            print("Finger not found")

    def del_finger(self):
        location = int(input("Enter id (1 - 127)"))
        if self._finger.delete_model(location=location) == adafruit_fingerprint.OK:
            print("Deleted!")
        else:
            print("Failed to delete")
