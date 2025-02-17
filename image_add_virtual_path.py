import geopandas as gpd
import pandas as pd

#add image path as a property in a GeoJSON feature collection. Currently the images are hosted on Github

# GeoJSON files
data = r'C:\GitHub\ALD-Georef-Photo-map\ALD_photos_17Feb2025.json'

gdf = gpd.read_file(data)
image_base_path = "https://raw.githubusercontent.com/cnorton27/ALD-Georef-Photo-map/main/ALD_photos_2024_processed/"


for index, row in gdf.iterrows():
    imgname = row['name']
    image_full_path = image_base_path + imgname + ".jpg"

    gdf.loc[index, 'image_path'] = str(image_full_path)

gdf.to_file("ALD_imagecol_17Feb2025.geojson", driver='GeoJSON')


