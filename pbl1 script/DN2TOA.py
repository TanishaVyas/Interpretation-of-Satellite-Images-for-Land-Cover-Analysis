import rasterio
import numpy as np
import os

def dn_to_toa(dn_file, output_file):
    """
    Convert a Sentinel-2 DN TIFF file to TOA reflectance without using sun elevation angle.

    Parameters:
    - dn_file: Path to the input DN TIFF file.
    - output_file: Path to save the output TOA reflectance TIFF file.
    """
    # Reflectance scaling factor for Sentinel-2 Level-1C
    reflectance_scaling_factor = 0.0001

    # Open the DN TIFF file
    with rasterio.open(dn_file) as src:
        dn_data = src.read(1)  # Read the first band
        profile = src.profile  # Get the metadata

    # Convert DN to TOA reflectance
    toa_reflectance = dn_data * reflectance_scaling_factor

    # Update the metadata for the output file
    profile.update(dtype=rasterio.float32, count=1)

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the TOA reflectance to a new TIFF file
    with rasterio.open(output_file, 'w', **profile) as dst:
        dst.write(toa_reflectance.astype(rasterio.float32), 1)

    print(f"TOA reflectance saved to {output_file}")

# Example usage
dn_file = 'C:\Tanisha(new)\gis\pbl1\processed tif\R20\B02.tif'  # Path to the input DN TIFF file
output_file = 'C:/Tanisha(new)/gis/pbl1/processed tif/TOA.tif'  # Output file path

dn_to_toa(dn_file, output_file)