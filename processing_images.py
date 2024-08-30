import geopandas as gpd
import pandas as pd

# Directory containing GeoJSON files
data = r'C:\Users\ciara\OneDrive\Documents\GitHub\ALD-Georef-Photo-map\ALD_photos.json'

# https://raw.githubusercontent.com/cnorton27/ALD-Georef-Photo-map/main/ALD_photos_2024_processed/IMG_5411.jpg
                
gdf = gpd.read_file(data)
image_base_path = "https://raw.githubusercontent.com/cnorton27/ALD-Georef-Photo-map/main/ALD_photos_2024_processed/"

for index, row in gdf.iterrows():
    imgname = row['name']
    image_full_path = image_base_path + imgname + ".jpg"

    gdf.loc[index, 'image_path'] = str(image_full_path)

gdf.to_file("ALDs_processed.geojson", driver='GeoJSON')