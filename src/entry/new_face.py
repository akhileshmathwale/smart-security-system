import os
import time
import cv2
import numpy as np

from ..constant import (
    CASCADE_FILE, VID_WIDTH, VID_HEIGHT, DELAY, DATASET, IMAGE_COUNT, TRAINED_FILE, CAMERA_ID
)
from ..database import DataStore

# initializing the classifier
face_detector = cv2.CascadeClassifier(CASCADE_FILE)

# recognizer classifier
recognizer = cv2.face.LBPHFaceRecognizer_create()


def add_new_entry():
    if not os.path.isdir(DATASET):
        os.mkdir(DATASET)

    cam = cv2.VideoCapture(CAMERA_ID)
    cam.set(3, VID_WIDTH)  # set video width
    cam.set(4, VID_HEIGHT)  # set video height

    face_name = input("Enter the name for the person :: ")
    face_id = DataStore.write(str(face_name))
    print("[INFO] Initializing face capture. Look the camera and wait ...")

    count = 0
    faces, ids = list(), list()

    while count < IMAGE_COUNT:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in face:
            print("Face detected.")

            # Save the captured image into the datasets folder
            cv2.imwrite(f"{DATASET}/user_" + str(face_id) + '_' + str(count) + ".jpg", gray[y:y + h, x:x + w])
            count += 1

            faces.append(gray[y: y + h, x: x + w])
            ids.append(face_id)

        # waiting for new image
        time.sleep(DELAY)

    recognizer.train(faces, np.array(ids))
    recognizer.write(TRAINED_FILE)
    print(f"[INFO] {len(np.unique(ids))} faces trained...")

    # Do a bit of cleanup
    print("[INFO] Exiting Program and cleanup stuff")
    cam.release()
