#pip install piexif exif pillow_heif

#import libraries
from PIL.ExifTags import TAGS
#import piexif
import exif
from exif import Image
import os
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
from datetime import datetime
import re
import geopandas as gpd
import pandas as pd


#code adapted from https://stackoverflow.com/questions/54395735/how-to-work-with-heic-image-file-types-in-python
#converts .HEIC to JPG (keeps original) AND reduces size to 25% quality

register_heif_opener()

def convert_heic_to_jpeg(dir_of_interest):
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
                        image.save(dir_of_interest + "/" + os.path.splitext(filename)[0] + ".jpg", "jpeg", exif= exif_bytes)
                else:
                        print(f"Unable to get exif data for {filename}")

#Execute jobs here:
Directory = r'C:\Users\ciara\OneDrive\Documents\GitHub\ALD-Georef-Photo-map\ALD_photos_2024_raw'
Output_directory = r'C:\Users\ciara\OneDrive\Documents\GitHub\ALD-Georef-Photo-map\ALD_photos_2024_processed'

#convert_heic_to_jpeg(Directory)

