from image2geojson import features2collection
from image_add_virtual_path import adding_path
from HEIC_to_jpg_processsing import convert_heic_to_jpeg

#This script takes directories of photos organized into categories (e.g. Flood, ALD/Slump, Drone, Vegetation) and converts into geojson feature
#collection with properties including metadata on: photo coordinates, date and time taken, category and link to web-hosted photo

#Use main.py to process photos into jpg (if not in jpg already), convert into feature collection and attach web-hosted link

#Image directories
ALD_photos = r'Data\ALD_photos_2024'
flood_photos = r'Data\FloodPhotos'

#Output jeojson files
ALD_geojson = r'Data\Flood_photos_18Feb2025.geojson' #formerly .json
flood_geojson = ''
veg_geojson = ''
drone_geojson = ''

# Example usage:
# features2collection('/path/to/images', '/path/to/output.geojson', 'string of dataset category")

#features2collection(flood_photos, output_geojson, "Flood")
ALD_df = features2collection(ALD_photos, "ALD/Slump")
#features2collection(veg_photos, output_geojson, "Vegetation")
#features2collection(Drone_photos, output_geojson, "Drone")

#Use image_add_virtual_path.py script to add virtual file paths as a property to feature collection


image_base_path = "https://raw.githubusercontent.com/cnorton27/ALD-Georef-Photo-map/main/Data/ALD_photos_2024_processed/"
out_path = r'Data\testing2.geojson'

adding_path(image_base_path, ALD_df, out_path)
