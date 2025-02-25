from image2geojson import features2collection
from image_add_virtual_path import adding_path
from HEIC_to_jpg_processsing import convert_heic_to_jpeg
import glob
import os
import geopandas as gpd
import pandas as pd

#This script takes directories of photos organized into categories (e.g. Flood, ALD/Slump, Drone, Vegetation) and converts into geojson feature
#collection with properties including metadata on: photo coordinates, date and time taken, category and link to web-hosted photo

#Image directories
ALD_photos = r'Data\ALD_photos'
flood_photos = r'Data\flood_photos'
veg_photos = r'Data\veg_photos' 
drone_photos = r'Data\drone_photos' 

#Output geojson files
ALD_geojson = r'Data\ALD_photos.geojson' 
flood_geojson = r'Data\flood_photos.geojson' 
veg_geojson = r'Data\veg_photos.geojson' 
drone_geojson = r'Data\drone_photos.geojson' 

#Use convert_heic_to_jpeg to process photos into jpg (if not in jpg already), convert into feature collection and attach web-hosted link. Adds a copy of photo as jpg in directory

#convert_heic_to_jpeg(flood_photos)
#convert_heic_to_jpeg(veg_photos)
#convert_heic_to_jpeg(ALD_photos)

#use features2collection to convert photo dir into geodataframe with each photo as a feature

ALD_df = features2collection(ALD_photos, "ALD/Slump")
flood_df = features2collection(flood_photos, "Flood")
veg_df = features2collection(veg_photos, "Vegetation")
drone_df = features2collection(drone_photos, "Drone")

#use adding_path to add web-hosted path to image

ALD_image_base_path = "https://raw.githubusercontent.com/cnorton27/ALD-Georef-Photo-map/refs/heads/main/Data/ALD_photos/"
adding_path(ALD_image_base_path, ALD_df, ALD_geojson)

flood_image_base_path = "https://raw.githubusercontent.com/cnorton27/ALD-Georef-Photo-map/refs/heads/main/Data/flood_photos/"
adding_path(flood_image_base_path, flood_df, flood_geojson)

veg_image_base_path = "https://raw.githubusercontent.com/cnorton27/ALD-Georef-Photo-map/refs/heads/main/Data/veg_photos/"
adding_path(veg_image_base_path, veg_df, veg_geojson)

drone_image_base_path = "https://raw.githubusercontent.com/cnorton27/ALD-Georef-Photo-map/refs/heads/main/Data/drone_photos/" #"https://cnorton27.github.io/ALD-Georef-Photo-map/Data/drone_photos"   #"https://raw.githubusercontent.com/cnorton27/ALD-Georef-Photo-map/refs/heads/main/Data/drone_photos/"
adding_path(drone_image_base_path, drone_df, drone_geojson)

#combine feature collections:
data_dir = r'Data'

# Get a list of all GeoJSON files in the directory
geojson_files = glob.glob(os.path.join(r'Data', '*.geojson'))

gdfs = []
# Iterate over each GeoJSON file and load it into GeoDataFrame
for file in geojson_files:
    gdf = gpd.read_file(file)
    gdfs.append(gdf)

output = r'Data\all_photos.geojson'

combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
combined_gdf.to_file(output, driver='GeoJSON')