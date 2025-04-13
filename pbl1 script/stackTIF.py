import os
from osgeo import gdal

input_folder = r"C:\Tanisha(new)\gis\pbl1\processed tif\R20"
output_folder = r"C:\Tanisha(new)\gis\pbl1\stacked tif\R20"
os.makedirs(output_folder, exist_ok=True)

bands = ["B02", "B03", "B04", "B05", "B06", "B07","B8A","B11", "B12"]

resampled_folder = os.path.join(output_folder, "resampled")
os.makedirs(resampled_folder, exist_ok=True)

# Resample all bands to 20m
for band in bands:
    input_path = os.path.join(input_folder, f"{band}.tif")
    output_path = os.path.join(resampled_folder, f"{band}_20m.tif")

    if not os.path.exists(input_path):
        print(f"Skipping {band}, file not found.")
        continue

    # Resample to 20m resolution
    gdal.Warp(output_path, input_path, xRes=20, yRes=20, resampleAlg="bilinear")
    print(f"Resampled {band} to 20m")

# Stack resampled bands
stacked_output = os.path.join(output_folder, "stacked_all_20m.tif")

# list of resampled band files
band_files = [os.path.join(resampled_folder, f"{band}_20m.tif") for band in bands if os.path.exists(os.path.join(resampled_folder, f"{band}_20m.tif"))]

# Use gdal.BuildVRT with separate=True to stack bands
vrt_output = stacked_output.replace(".tif", ".vrt")
gdal.BuildVRT(vrt_output, band_files, separate=True)

# Convert VRT to GeoTIFF
gdal.Translate(stacked_output, vrt_output, format="GTiff")

print(f"Created single stacked file: {stacked_output}")