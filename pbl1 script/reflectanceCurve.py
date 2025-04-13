import rasterio
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline  # For spline interpolation

# Define file path for the R20m stacked image
stacked_image_path = r"C:\\Tanisha(new)\\gis\\pbl1\\stacked tif\\R20\\stacked_all_20m.tif"

# Define wavelengths for the bands (in micrometers)
wavelengths = [0.490, 0.560, 0.665, 0.705, 0.740, 0.783, 0.842, 1.610, 2.190]

# Open the stacked image
with rasterio.open(stacked_image_path) as src:
    # Read all bands
    bands = src.read()  # Shape: (num_bands, height, width)
    num_bands = src.count
    height, width = bands.shape[1], bands.shape[2]

    # Reshape the bands to (height * width, num_bands)
    dn_bands = bands.reshape(num_bands, -1).T  # Shape: (height * width, num_bands)

# Convert DN to NToA Reflectance
ntoa_bands = dn_bands / 10000.0 * 100  # ToA Reflectance in %

# Define thresholds for classification
blue_band_index = 0
nir_band_index = 6  # Band 8 (NIR) is index 6 in the stacked image
red_band_index = 2   # Band 4 (Red) is index 2 in the stacked image
swir1_band_index = 7 # Band 11 (SWIR1) is index 7 in the stacked image
swir2_band_index = 8 # Band 12 (SWIR2) is index 8 in the stacked image

# Initialize classification array
classification = np.zeros(height * width, dtype=int)  # 0 = Unclassified, 1 = Water, 2 = Vegetation, 3 = Construction

# Classify pixels
for i, pixel in enumerate(ntoa_bands):
    blue = pixel[blue_band_index]
    nir = pixel[nir_band_index]
    red = pixel[red_band_index]
    swir1 = pixel[swir1_band_index]
    swir2 = pixel[swir2_band_index]

    # Water: Low reflectance in NIR and SWIR
    if blue < 12 and nir < 12 and swir1 < 12 and swir2 < 12:  
        classification[i] = 1  # Water

    # Vegetation: High NIR, low Red
    elif nir > 18 and red < 20:  
        classification[i] = 2  # Vegetation

    # Construction: Moderate reflectance across all bands
    else:
        classification[i] = 3  # Construction

# Extract reflectance values for each land cover type
reflectance_values = {
    "Water": [],
    "Vegetation": [],
    "Construction": []
}

for land_cover, value in zip(classification, ntoa_bands):
    if land_cover == 1:  # Water
        reflectance_values["Water"].append(value)
    elif land_cover == 2:  # Vegetation
        reflectance_values["Vegetation"].append(value)
    elif land_cover == 3:  # Construction
        reflectance_values["Construction"].append(value)

# Print number of pixels for each land cover type
for land_cover, values in reflectance_values.items():
    print(f"{land_cover}: {len(values)} pixels")

# Print reflectance values for the first 10 pixels
print("Reflectance values for the first 10 pixels:")
for i in range(10):
    print(f"Pixel {i}: {ntoa_bands[i]}")

# Calculate mean reflectance for each land cover type (only if pixels exist)
mean_reflectance = {}
for land_cover, values in reflectance_values.items():
    if len(values) > 0:  
        mean_reflectance[land_cover] = np.mean(values, axis=0)
        print(f"Mean reflectance for {land_cover}: {mean_reflectance[land_cover]}")

# Plot the graph: Wavelength vs Reflectance (with smooth curves)
plt.figure(figsize=(10, 6))

# Generate smooth curves using spline interpolation
x_new = np.linspace(min(wavelengths), max(wavelengths), 300)  

for land_cover, values in mean_reflectance.items():
    # Create a spline interpolation function
    spline = make_interp_spline(wavelengths, values, k=3)  # k=3 for cubic spline
    y_new = spline(x_new)  # Interpolate y-values for the smooth curve

    # Plot the smooth curve
    plt.plot(x_new, y_new, linestyle='-', label=land_cover)

# Customize the graph
plt.title('Spectral Reflectance of Land Cover Types')
plt.xlabel('Wavelength (micrometers)')
plt.ylabel('Reflectance (%)')
plt.legend()
plt.grid(True)

# Set x-axis limits and ticks
plt.xlim(0.4, 2.4)
plt.xticks(np.arange(0.4, 2.5, 0.2))

# Show the graph
plt.show()
