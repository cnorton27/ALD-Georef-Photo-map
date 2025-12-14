#pip install piexif exif pillow_heif gpsphoto exifread

#import libraries
from PIL.ExifTags import TAGS
import piexif
import exif
from exif import Image
import os
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
from datetime import datetime
import piexif
import re
import geopandas as gpd
import pandas as pd
from GPSPhoto import gpsphoto
from GPSPhoto.gpsphoto import GPSInfo
import os
import exifread
import glob
import itertools

dir1 = r"D:\KLU_Drone_Data_2025\HogePass-sheep_13Jul2025\100_0009"
dir2 = r"D:\KLU_Drone_Data_2025\HogePass-sheep_13Jul2025\100_0010"
dir3 = r"D:\KLU_Drone_Data_2025\HogePass-sheep_13Jul2025\100_0011"

image_list1 = glob.glob(os.path.join(dir1, "**", "*.[jJ][pP][gG]"), recursive=True)
image_list2 = glob.glob(os.path.join(dir2, "**", "*.[jJ][pP][gG]"), recursive=True)
image_list3 = glob.glob(os.path.join(dir3, "**", "*.[jJ][pP][gG]"), recursive=True)

image_list_new = list(itertools.chain(image_list3, image_list2, image_list1))

def maxminlatlong(image_dir):
    """
    Takes an image dir of JPEGS and returns the geographical extent of the imagery in latitude and llongitude coordinates
    """
    #image_list = glob.glob(os.path.join(image_dir, "**", "*.JPG"), recursive = True)
    #image_list = glob.glob(os.path.join(image_dir, "**", "*.[jJ][pP][gG]"), recursive=True)

    image_list = image_list_new

    print(image_list)

    #image_list = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

    latitudes = []
    longitudes = []

    for i in image_list:
         lat = get_lat(i)
         lon = get_long(i)
         latitudes.append(lat)
         longitudes.append(lon)

    lat_filter = list(filter(lambda x: x != [0, 0], latitudes))
    latitudes = lat_filter

    max_lat = max(latitudes)
    min_lat = min(latitudes)
    max_long = max(longitudes)
    min_long = min(longitudes)

    print("Max latitude", max_lat, "Min latitude", min_lat, "Max longitude", max_long, "Min longitude", min_long)




def get_long(image_path):
    """
    Retrieves GPS data from the given image.
    """
    data = gpsphoto.getGPSData(image_path)
    if data is None:
        print(f"Warning: No GPS data found for {image_path}.")
        return None  # or return default coordinates if needed

    latitude = data.get('Latitude')
    longitude = data.get('Longitude')

    if latitude is None or longitude is None:
        #print(f"Warning: Missing Latitude or Longitude for {image_path}.")
        return [0, 0]

    return [longitude]  # Ensure the order is [longitude, latitude]


def get_lat(image_path):
    """
    Retrieves GPS data from the given image.
    """
    data = gpsphoto.getGPSData(image_path)
    if data is None:
        print(f"Warning: No GPS data found for {image_path}.")
        return None  # or return default coordinates if needed

    latitude = data.get('Latitude')
    longitude = data.get('Longitude')

    if latitude is None or longitude is None:
        #print(f"Warning: Missing Latitude or Longitude for {image_path}.")
        return [0, 0]

    return [latitude]  # Ensure the order is [longitude, latitude]

dir = r"D:\KLU_Drone_Data_2025\HogePass-sheep_13Jul2025"

maxminlatlong(dir)




