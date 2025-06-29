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
import geopandas as gpd
from rasterio.mask import mask
# from rasterio.windows import from_bounds

# Define the paths to the raster file and the AOI vector file
gfw_raster_file = r"C:\Users\Carol\Dropbox\GIS\Projects\IOB_AlbertineRift\1_raw_data\raster\gfw_alerts\20250218\00N_020E.tif"
aoi_vector_path = r"C:\Users\Carol\Dropbox\GIS\Projects\IOB_AlbertineRift\2_intermediate_data\AlbertineRift_data.gpkg"

# Read AOI geometries
layer_name = "aoi_buffer_10km_4326"
vector_features = gpd.read_file(aoi_vector_path, layer=layer_name)

# Print the number of AOI features
num_features = len(vector_features)
print(f"Number of AOI features: {num_features}")

# Open the raster file
with rasterio.open(gfw_raster_file) as src:
     # Loop over each AOI feature
    for idx, aoi in vector_features.iterrows():
        geom = [aoi['geometry']]
        aoi_name = aoi['aoi_name']  # Replace with the actual field name for AOI name

        # Mask the raster data with the current AOI
        out_image, out_transform = mask(src, geom, crop=True)
        data = out_image[0]

        # Get the spatial information from the raster file
        transform = out_transform
        width = data.shape[1]
        height = data.shape[0]

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
                # conf = int(str(alert)[0])
                days = int(str(alert)[1:])
                date = np.datetime64('2014-12-31') + np.timedelta64(days, 'D')
                
                # Convert the pixel coordinates to longitude and latitude
                lon, lat = rasterio.transform.xy(transform, y, x)
                
                # Add the data to the output list
                output.append([alert_id, lon, lat, date, conf, aoi_name])

                # Increment the alert ID counter
                alert_id += 1

        # Print the number of alerts that fit the criteria
        num_alerts = len(output)
        print(f"Number of alerts {aoi_name}: {num_alerts}")

        # Write the output list to a CSV file
        # with open('\data\GFW_20250218_alerts.csv', 'w', newline='') as f:
        if not output:
            print("No data to write to CSV for {aoi_name}.")
        # else:
        else:
            output_csv_path = rf"C:\Users\Carol\Dropbox\GIS\Projects\IOB_AlbertineRift\2_intermediate_data\gfw_alerts\GFW_{aoi_name}.csv"
            # output_csv_path = r"C:\Users\Carol\Dropbox\GIS\Projects\IOB_AlbertineRift\2_intermediate_data\gfw_alerts\GFW_20250218_alerts_aoi.csv"
            try:
                with open(output_csv_path, 'w', newline='') as f:
        # with open('C:\Users\Carol\Dropbox\GIS\Projects\IOB_AlbertineRift\1_raw_data\raster\gfw_alerts\GFW_20250218_alerts.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Alert_ID', 'Longitude', 'Latitude', 'Date', 'Confidence', 'AOI_Name'])
                    writer.writerows(output)
                print(f"Data successfully written to {output_csv_path}")
            except Exception as e:
                print(f"An error occurred: {e}")

print("Processing complete.")