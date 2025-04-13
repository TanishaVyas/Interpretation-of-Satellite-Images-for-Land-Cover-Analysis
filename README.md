# Land Cover Analysis using Sentinel-2 Imagery

## Project Overview

This project focuses on analyzing land cover using satellite imagery from Sentinel-2. The objective is to interpret spectral bands to classify regions into vegetation, water bodies, and built-up areas using reflectance data.

---

## Data Used

- **Sentinel-2** satellite images (13-band multispectral data)
- Copernicus Open Access Hub for image sourcing

---

## Key Processes

- Downloading and preprocessing Sentinel-2 imagery
- Converting `.jp2` bands to `.tif` format
- Converting Digital Number (DN) values to TOA reflectance
- Stacking multiple bands into a single GeoTIFF
- Classifying land cover types
- Generating spectral reflectance plots for analysis

---

## Results

- Successfully generated reflectance curves for:
  - **Water**
  - **Vegetation**
  - **Construction**
- The spectral graph shows distinct patterns for each land cover type, aiding in accurate classification.

---

## References

- [QGIS Documentation](https://docs.qgis.org/3.34/en/docs/user_manual/index.html)  
- [Copernicus Browser](https://browser.dataspace.copernicus.eu)  
- [GDAL](https://gdal.org/en/stable/)  
- [Rasterio](https://rasterio.readthedocs.io/en/stable/)
