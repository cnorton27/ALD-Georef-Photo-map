import geopandas as gpd
import pandas as pd

#add image path as a property in a GeoJSON feature collection. Currently the images are hosted on Github

# GeoJSON files
data = r'C:\GitHub\ALD-Georef-Photo-map\ALD_photos_17Feb2025.json'
image_base_path = "https://raw.githubusercontent.com/cnorton27/ALD-Georef-Photo-map/main/ALD_photos_2024_processed/"
GoogleDriveFloodPath = 'https://drive.google.com/drive/folders/14-0CFHuW5e4JxWzl5tU7qH1_5WTj1io7?usp=drive_link'
out_path = r'C:\GitHub\ALD-Georef-Photo-map\testing.geojson'
Flood_JSON = r'C:\GitHub\ALD-Georef-Photo-map\Flood_photos_17Feb2025.json'

def adding_path(image_dir, geojson, output_path):
    """
    Takes an image directory (str), geojson (.json/.geojson) and output path (str) and adds image directory as =
    a property to each feature in geojson feature collection. Path links to photo feature.
    """

    gdf = gpd.read_file(geojson)

    for index, row in gdf.iterrows():
        imgname = row['name']
        image_full_path = image_dir + imgname + ".jpg"

        gdf.loc[index, 'image_path'] = str(image_full_path)

    gdf.to_file(output_path, driver='GeoJSON')
    
#example usage
#adding_path(image_base_path, data, out_path)

