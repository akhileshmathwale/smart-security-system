import os
import time
import cv2
import numpy as np

from ..constant import (
    CASCADE_FILE, VID_WIDTH, VID_HEIGHT, DELAY, DATASET, IMAGE_COUNT, TRAINED_FILE, CAMERA_ID
)
from ..database import DataStore
from ..exception import CameraOpeningError


class FaceEntry:
    def __init__(self):  
        # initializing the classifier
        self._face_detector = cv2.CascadeClassifier(CASCADE_FILE)

        # recognizer classifier
        self._recognizer = cv2.face.LBPHFaceRecognizer_create()

        self._cam = cv2.VideoCapture(CAMERA_ID)
        self._cam.set(3, VID_WIDTH)  # set video width
        self._cam.set(4, VID_HEIGHT)  # set video height

    def add_new_entry(self):
        if not os.path.isdir(DATASET):
            os.mkdir(DATASET)

        face_name = input("Enter the name for the person :: ")
        face_id = DataStore.write(str(face_name))
        print("[INFO] Initializing face capture. Look the camera and wait ...")

        count = 0
        faces, ids = list(), list()

        while count < IMAGE_COUNT:
            ret, img = self._cam.read()

            if not ret:
                raise CameraOpeningError(CAMERA_ID)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face = self._face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in face:
                print("Face detected.")

                # create new directory for new face
                if not os.path.isdir(str(f"{DATASET}/{face_id}")):
                    os.mkdir(str(f"{DATASET}/{face_id}"))

                # Save the captured image into the datasets folder
                cv2.imwrite(f"{DATASET}/{face_id}/user_" + str(face_id) + '_' + str(count) + ".jpg", gray[y:y + h, x:x + w])
                count += 1

                faces.append(gray[y: y + h, x: x + w])
                ids.append(face_id)

            # waiting for new image
            time.sleep(DELAY)

        # training the model
        self.train_model()

        # Do a bit of cleanup
        print("[INFO] Exiting Program and cleanup stuff")
        self._cam.release()


    def train_model(self):
        db = DataStore.get_all_ids()

        if isinstance(db, dict):
            ids = list(db.keys())  # from database ids
            faces = list()

            for id, count in zip(ids, range(3)):
                file = str(f"{DATASET}/{id}/user_" + str(id) + '_' + str(count) + ".jpg")
                faces.append(cv2.imread(file, cv2.IMREAD_GRAYSCALE))

            self._recognizer.train(faces, np.array(ids[: len(faces)]))
            self._recognizer.write(TRAINED_FILE)
            print(f"[INFO] {len(np.unique(ids))} faces trained...")
