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


def features2collection(image_dir, output_json_path, dataset_category):
  """
  Converts features feature collection and writes to a geojson file.
  """
  feature_list = features2list(image_dir, dataset_category)
  feature_coll = {
    "type": "FeatureCollection",
    "features": feature_list
  }
  
  df = gpd.GeoDataFrame.from_features(feature_coll["features"], crs="EPSG:4326")
  df.to_file(output_json_path, driver='GeoJSON')
  

def features2list(image_dir, dataset_category):
    """
Appends geojson features to a list
    """
    image_list = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

    feature_coll = []
    for i in image_list:
         finished_feature = image2json(i, dataset_category)
         feature_coll.append(finished_feature)
    return feature_coll
    

def image2json(image, dataset_category):
    """
    Converts images to a GeoJSON feature.
    """
    name = os.path.splitext(os.path.basename(image))[0] #was test_photo
    gps_data = get_gps_data(image)
    date_time = get_date_data(image)
    category = dataset_category

    return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": gps_data
            },
            "properties": {
                "name": name,
                "date": date_time,
                "category": category,
                "notes": ""
            }
        }

def get_gps_data(image_path):
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

    return [longitude, latitude]  # Ensure the order is [longitude, latitude]

def get_date_data(image_path):
    """
    Retrieves date time data from the given image.
    """
    photo = gpsphoto.getGPSData(image_path)
    
    if photo is None:
        print(f"Warning: No GPS data found for {image_path}.")
        return None  # Handle case where no GPS data is returned
    
    # Use .get() to safely retrieve 'Date' and 'UTC-Time', return 'Unknown' if they are missing
    date = photo.get("Date", "Unknown")
    utc_time = photo.get("UTC-Time", "Unknown")
    
    return [date, utc_time]




