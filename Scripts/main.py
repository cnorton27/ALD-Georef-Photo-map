import image2geojson
import image_add_virtual_path

output_geojson = r'C:\GitHub\ALD-Georef-Photo-map\Flood_photos_18Feb2025.json'
ald_photos = r'C:\GitHub\ALD-Georef-Photo-map\ALD_photos_2024_processed'
flood_photos = r'C:\GitHub\ALD-Georef-Photo-map\FloodPhotos'

# Example usage:
# features2collection('/path/to/images', '/path/to/output.geojson', 'string of dataset category")

#features2collection(flood_photos, output_geojson, "Flood")
#features2collection(ald_photos, output_geojson, "ALD/Slump")
#features2collection(veg_photos, output_geojson, "Vegetation")
#features2collection(Drone_photos, output_geojson, "Drone")

#Use image_add_virtual_path.py script to add virtual file paths as a property to feature collection

from image_add_virtual_path import adding_path

data = r'Data\ALD_photos_with_path.geojson'
image_base_path = "https://raw.githubusercontent.com/cnorton27/ALD-Georef-Photo-map/main/Data/ALD_photos_2024_processed/"
out_path = r'Data\ALD_photos_with_path.geojson'

adding_path(image_base_path, data, out_path)
