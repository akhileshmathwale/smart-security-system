# cascade file
CASCADE_FILE = "./src/cascade/haarcascade_frontalface_default.xml"

# trained file
TRAINED_FILE = "./src/trainer/trainer.yml"

# camera capture id
CAMERA_ID = 0

# input cam height, width
VID_WIDTH = 480
VID_HEIGHT = 480

# delay for picture capture
DELAY = 2

# datastore specific
DB_FILE = "./src/database/datastore.db"

# images dataset folder
DATASET = "./src/dataset"
IMAGE_COUNT = 3

# minimum face detection confidence (0 is accurate)
MIN_FACE_CONF = 60

# threshold for motion detection
MOTION_THRESHOLD = 50

# motion sensor values
MS_IN_PIN = 21
MS_DELAY = 0.1

# finger sensor values
# min no of prints
MIN_FINGER_PRINTS = 5

# communication ids
COMM_MOTION_DETECTED = "motion_detected"
COMM_FACE_DETECTED = "face_detected"
