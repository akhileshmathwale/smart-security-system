import cv2

from ..constant import (
    CASCADE_FILE, TRAINED_FILE, VID_WIDTH, VID_HEIGHT, MIN_FACE_CONF, CAMERA_ID, COMM_FACE_DETECTED
)
from ..database import DataStore
from ..exception import CameraOpeningError


class Recognize:
    def __init__(self):
        self._stop = False
        self._recognizer = cv2.face.LBPHFaceRecognizer_create()
        self._classifier = cv2.CascadeClassifier(CASCADE_FILE)
        self._recognizer.read(TRAINED_FILE)

        self._cam = cv2.VideoCapture(CAMERA_ID)
        self._cam.set(3, VID_WIDTH)
        self._cam.set(4, VID_HEIGHT)

    def stop(self):
        self._stop = True
        self._cam.release()

    def recognize(self, comm):
        print("waiting for face")
        while not self._stop:
            ret, img = self._cam.read()

            if not ret:
                raise CameraOpeningError(CAMERA_ID)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self._classifier.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5
            )

            for (x, y, w, h) in faces:
                id_, confidence = self._recognizer.predict(gray[y: y + h, x: x + w])

                if confidence < MIN_FACE_CONF:
                    print(f"[INFO] {DataStore.read(id_)} face detected.")
                    comm.send(COMM_FACE_DETECTED)

                else:
                    print(f"[INFO] Unknown face detected.")
