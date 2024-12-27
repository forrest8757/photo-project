import os
import imagehash
import shutil
import pickle
from PIL import Image, ExifTags


#PATHS
#TODO: probably have it write these folders out into the project dir just so we can have everything working in one spot.
# since rn it throws errors if you dont have the right folders
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
            # TODO: check to see if there is a folder that has been created for deleted, clean etc. if not there make dir, currently throwing exception
            shutil.move(item_path, os.path.join(deleted_path, item))
        else:
            # move to clean dir and put hashed id into photo_id
            # TODO: check to see if there is a folder that has been created for clean etc. if not there make dir, currently throwing exception
            photo_id[hash1]=0
            shutil.move(item_path, os.path.join(clean_path, item))
    except Exception as e:
        print(f"Error processing '{item}': {e}")

    #TODO: open and read file to see if there is any meta data that we can extract.
    img = Image.open(item_path)
    exif = {ExifTags.TAGS[k]: v for k, v in img.getexif().items() if k in ExifTags.TAGS}
    print(exif)

    #TODO: process image and see if there is anything that you can visually extract from the image to understand what its about


    #TODO: scan image off faces we know/have trained on
    # open CV

    #TODO: extract text from image
    # open cv might be able to do something

    #TODO: extract location data if available
    # https://stackoverflow.com/questions/67037083/cant-get-gps-coordinates-from-from-exif-data-in-python-pillow-or-pyexiv2
    # https://github.com/python-pillow/Pillow/issues/5863#issuecomment-984917141
    # https://stackoverflow.com/questions/19804768/interpreting-gps-info-of-exif-data-from-photo-in-python

    #TODO: process location data into country, city, etc


    #TODO: save image hash and meta data into a database of some kind so that we can keep track of what we have processes


    #TODO: on the app display a summary about the image/images.
    # eg: camera, date, location, filename, display small portion of the file.


with open(photo_id_path, "wb") as file:
    pickle.dump(photo_id, file)
    print("saved photo ids")
print(os.listdir(clean_path))
    

