import os
import imagehash
import shutil
import pickle
from PIL import Image


#PATHS

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
to_be_sorted_path = os.path.join(desktop_path, "tobesorted")
deleted_path = os.path.join(desktop_path, "deleted")
clean_path = os.path.join(desktop_path, "clean")
photo_id_path = os.path.join(desktop_path, "photo_id.pkl")



if not os.path.exists(to_be_sorted_path):
    print("the folder '{to_be_sorted_path}' does not exist")
else:
    print(f"the folder '{to_be_sorted_path}' exist")


#load pickle file if they exist or create a new one
if os.path.exists(photo_id_path):
    with open(photo_id_path, "rb") as file:
        photo_id = pickle.load(file)
    print("loaded existing photo hashes")
else:
    photo_id = {}
    print("no existing photo hashes found")


contents = os.listdir(to_be_sorted_path)
print(contents)
# iterate over each photo in to_be_sorted dir
for item in contents:
    item_path = os.path.join(to_be_sorted_path, item)
    
    # Skip hidden files like '.DS_Store'
    if item.startswith('.'):
        continue
    try:
            
        hash1 = imagehash.phash(Image.open(item_path))
        if hash1 in photo_id:
            # move photo into deleted dir
            shutil.move(item_path, os.path.join(deleted_path, item))
        else:
            # move to clean dir and put hashed id into photo_id
            photo_id[hash1]=0
            shutil.move(item_path, os.path.join(clean_path, item))
    except Exception as e:
        print(f"Error processing '{item}': {e}")



with open(photo_id_path, "wb") as file:
    pickle.dump(photo_id, file)
    print("saved photo ids")
print(os.listdir(clean_path))
    

