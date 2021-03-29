import cv2

from ..constant import (
    CASCADE_FILE, TRAINED_FILE, VID_WIDTH, VID_HEIGHT, MIN_FACE_CONF, CAMERA_ID
)
from ..database import DataStore
from ..exception import CameraOpeningError


def recognize():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    classifier = cv2.CascadeClassifier(CASCADE_FILE)
    recognizer.read(TRAINED_FILE)

    cam = cv2.VideoCapture(CAMERA_ID)
    cam.set(3, VID_WIDTH)
    cam.set(4, VID_HEIGHT)

    # test
    count = 0

    while count < 20:
        ret, img = cam.read()

        if not ret:
            raise CameraOpeningError(CAMERA_ID)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = classifier.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:
            id_, confidence = recognizer.predict(gray[y: y + h, x: x + w])

            if confidence < MIN_FACE_CONF:
                print(f"[INFO] {DataStore.read(id_)} face detected.")
                count += 1
            else:
                print(f"[INFO] Unknown face detected.")
                count += 1

    cam.release()
