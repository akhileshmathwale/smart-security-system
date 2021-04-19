from .entry import add_new_entry
from .core import recognize, detect, setup, cleanup

print("Running the motion sensor")
setup()
cleanup()
print("Done")

