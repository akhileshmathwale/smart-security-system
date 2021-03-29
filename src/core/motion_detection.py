import time

import cv2
import numpy as np

from ..constant import (
    VID_WIDTH, VID_HEIGHT, CAMERA_ID, MOTION_THRESHOLD
)
from ..exception import CameraOpeningError


def detect():
    cam = cv2.VideoCapture(CAMERA_ID)
    cam.set(3, VID_HEIGHT)
    cam.set(4, VID_WIDTH)
    
    frame, first_frame = None, None
    
    while True:
        ret, frame = cam.read()
        
        if not ret:
            raise CameraOpeningError(CAMERA_ID)
            
        # converting to gray scale and blur
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (21, 21), 0)
        
        # storing for the first time
        if first_frame is None:
            first_frame = frame
            continue
            
        # calculating frame difference and threshing the values
        diff = cv2.absdiff(first_frame, frame)
        thresh = cv2.threshold(diff, MOTION_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
        
        # if greater than zero high diff in the frames
        thresh_max = np.max(thresh)
        if thresh_max > 0:
            print("Motion detected")
            
        first_frame = frame
    
    print("Done...")
