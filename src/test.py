from src.entry import add_new_finger, match_finger, del_finger

# print("Running the motion sensor")
# setup()
# cleanup()
# print("Done")

print("testing for finger sensor")
if add_new_finger():
    match_finger()  

#match_finger()    

# del_finger()