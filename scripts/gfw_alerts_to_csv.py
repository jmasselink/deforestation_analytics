# derived from a question to ChatGPT
# How could I use Python code to derive a CSV with 4 fields: longitude, latitude, date, and confidence level from a raster which has the following encoding/syntax?:
# Each pixel (alert) encodes the date of disturbance and confidence level in one integer value. The leading integer of the decimal representation is 2 for a low-confidence alert, 3 for a high-confidence alert, and 4 for an alert detected by multiple alert systems, followed by the number of days since December 31, 2014. 0 is the no-data value. For example:
# 20001 is a low confidence alert on January 1st, 2015
# 30055 is a high confidence alert on February 24, 2015
# 21847 is a low confidence alert on January 21, 2020
# 41847 is a highest confidence alert (detected by multiple alert systems) on January 21, 2020. Alert date represents the earliest detection
# 0 represents no alert

import rasterio
import numpy as np
import csv

# Open the raster file and read in the data
# with rasterio.open('path/to/raster/file.tif') as src:

# gfw_raster_file = "C:/Users/Carol/Dropbox/GIS/Projects/RFO_mining/1_raw_data/raster/GFW/20241023/10N_020E.tif"
gfw_raster_file = "C:\Users\Carol\Dropbox\GIS\Projects\IOB_AlbertineRift\1_raw_data\raster\gfw_alerts\20250218\00N_020E.tif"

with rasterio.open(gfw_raster_file) as src:
    data = src.read(1)

# Get the spatial information from the raster file
transform = src.transform
width = src.width
height = src.height

# Create a list to hold the output data
output = []

# Initialize the alert ID counter
alert_id = 1

# Loop over each pixel in the data array
for y in range(height):
    for x in range(width):
        # Get the alert value from the data array
        alert = data[y,x]
        
        # If the alert value is 0, skip to the next pixel
        if alert == 0:
            continue

        
        # Determine the confidence level and number of days since Dec 31, 2014
        conf = int(str(alert)[0])
        
        # Only process alert levels 3 or 4
        if conf not in [3, 4]:
            continue
        
        # Determine the confidence level and number of days since Dec 31, 2014
        conf = int(str(alert)[0])
        days = int(str(alert)[1:])
        date = np.datetime64('2014-12-31') + np.timedelta64(days, 'D')
        
        # Convert the pixel coordinates to longitude and latitude
        lon, lat = rasterio.transform.xy(transform, y, x)
        
        # Add the data to the output list
        output.append([lon, lat, date, conf])

        # Increment the alert ID counter
        alert_id += 1

# Write the output list to a CSV file
with open('\data\GFW_20241023_alerts.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Alert_ID', 'Longitude', 'Latitude', 'Date', 'Confidence'])
    writer.writerows(output)