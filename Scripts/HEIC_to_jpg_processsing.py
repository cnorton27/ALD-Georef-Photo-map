#pip install piexif exif pillow_heif

#import libraries
from PIL.ExifTags import TAGS
import piexif
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
    HEIC_files = [f for f in filenames if re.search(r"\.HEIC$|\.heic$", f)]

    for filename in HEIC_files:
        image_path = os.path.join(dir_of_interest, filename)
        image = Image.open(image_path)
        image_exif = image.getexif()

        if image_exif:
            # Map tag names to values
            exif = {ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes}
            
            # Debug: Print available EXIF keys
            print(f"EXIF keys for {filename}: {list(exif.keys())}")

            # Handle missing 'DateTime' field
            date = None
            if 'DateTime' in exif:
                try:
                    date = datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S')
                except ValueError:
                    print(f"Warning: Unexpected date format in {filename}: {exif['DateTime']}")
            else:
                print(f"Warning: No DateTime metadata found in {filename}")

            # Load existing EXIF data
            exif_dict = piexif.load(image.info.get("exif", b""))

            # Update EXIF fields safely
            if date:
                exif_dict["0th"][piexif.ImageIFD.DateTime] = date.strftime("%Y:%m:%d %H:%M:%S")
            exif_dict["0th"][piexif.ImageIFD.Orientation] = 1
            exif_bytes = piexif.dump(exif_dict)

            # Save as JPEG
            output_path = os.path.join(dir_of_interest, os.path.splitext(filename)[0] + ".jpeg")
            image.save(output_path, "jpeg", exif=exif_bytes)
            
        else:
            print(f"Unable to get EXIF data for {filename}")
            exif_bytes = piexif.dump(exif_dict)
            image.save(output_path, "jpeg", exif=exif_bytes)


#Execute jobs here:
Directory = r'Data\drone_photos'
Directory = r"C:\Users\ciara\Downloads\Receipts June 5 -20250629T024706Z-1-001\Receipts June 5"
convert_heic_to_jpeg(Directory)

