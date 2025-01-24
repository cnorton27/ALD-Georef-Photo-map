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

#code adapted from https://stackoverflow.com/questions/54395735/how-to-work-with-heic-image-file-types-in-python
#converts .HEIC to JPG (keeps original) AND reduces size to 25% quality

def convert_heic_to_jpeg(dir_of_interest, out_dir):
        filenames = os.listdir(dir_of_interest)
        filenames_matched = [re.search(r"\.HEIC$|\.heic$", filename) for filename in filenames]

        # Extract files of interest
        HEIC_files = []
        for index, filename in enumerate(filenames_matched):
                if filename:
                        HEIC_files.append(filenames[index])

        # Convert files to jpg while keeping the timestamp
        for filename in HEIC_files:
                image = Image.open(dir_of_interest + "/" + filename)
                image_exif = image.getexif()
                if image_exif:
                        # Make a map with tag names and grab the datetime
                        exif = { ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes }
                        date = datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S')

                        # Load exif data via piexif
                        exif_dict = piexif.load(image.info["exif"])

                        # Update exif data with orientation and datetime
                        exif_dict["0th"][piexif.ImageIFD.DateTime] = date.strftime("%Y:%m:%d %H:%M:%S")
                        exif_dict["0th"][piexif.ImageIFD.Orientation] = 1
                        exif_bytes = piexif.dump(exif_dict)

                        # Save image as jpeg
                        image.save(out_dir + "/" + os.path.splitext(filename)[0] + ".jpg", "jpeg", exif= exif_bytes) #add quality=25 to reduce size
                else:
                        print(f"Unable to get exif data for {filename}")

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
    
    if 'DateTime' in photo:
        return photo['DateTime']
    else:
        print("Date-Time information is not available.")
        return None  # Explicitly return None if 'DateTime' is not found

def features2collection(image_dir, output_json_path, dataset_category):
  """
  Converts features feature collection and writes to a geojson file.
  """
  feature_list = features2list(image_dir, dataset_category)
  feature_coll = {
    "type": "FeatureCollection",
    "features": [feature_list]
  }
  df = gpd.GeoDataFrame.from_features(feature_coll)
  df.to_file(output_json_path, driver='GeoJSON')

def features2list(features, dataset_category):
    """
Appends geojson features to a list
    """
    feature_coll = []
    for i in features:
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

output_geojson = r'C:\GitHub\ALD-Georef-Photo-map\ALD_photos_13Jan2024.json'
ald_photos = r'C:\GitHub\ALD-Georef-Photo-map\ALD_photos_2024_processed'
# Example usage:
# features2collection('/path/to/images', '/path/to/output.geojson', 'string of dataset category")

#features2collection(ald_photos, output_geojson, "ALD/Slump")


test_photo = r'C:\GitHub\ALD-Georef-Photo-map\ALD_photos_2024_processed\IMG_6573.jpg'

image2json(test_photo, "ALD")

#get_date_data(test_photo)


