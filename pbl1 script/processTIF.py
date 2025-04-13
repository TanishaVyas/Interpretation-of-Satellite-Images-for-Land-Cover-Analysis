import os
from osgeo import gdal

input_folder = "C:\\Users\\Tanisha\\Downloads\\S2B_MSIL2A_20250106T054129_N0511_R005_T43QBC_20250106T080057.SAFE\\S2B_MSIL2A_20250106T054129_N0511_R005_T43QBC_20250106T080057.SAFE\\GRANULE\\L2A_T43QBC_A040929_20250106T055300\\IMG_DATA\\R60m"
output_folder = "C:\\Tanisha(new)\\gis\\pbl1\\processed tif\\R60"

os.makedirs(output_folder, exist_ok=True)

# List of bands to convert
bands = ["B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B11", "B12"]

for band in bands:
    input_path = os.path.join(input_folder, f"T43QBC_20250106T054129_{band}_60m.jp2")
    output_path = os.path.join(output_folder, f"{band}.tif")

    # Check if file exists
    if not os.path.exists(input_path):
        print(f"ERROR: {input_path} not found! Skipping...")
        continue

    # Try opening the file in GDAL
    dataset = gdal.Open(input_path)
    if dataset is None:
        print(f"ERROR: Could not open {input_path}")
        continue  # Skip to next file

    # Convert .jp2 to .tif
    gdal.Translate(output_path, dataset, format="GTiff")
    print(f"Converted {band} to GeoTIFF: {output_path}")