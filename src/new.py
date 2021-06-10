from src.entry import FingerEntry
from src.entry import FaceEntry


face_entry = FaceEntry()
finger_entry = FingerEntry()
# finger_entry.initialize()  # looks for the sensor [comment if not connected]

print("testing for finger sensor")
if finger_entry.add_new_finger():
    finger_entry.match_finger()  

print("waiting for adding new face entry")
face_entry.add_new_entry()
