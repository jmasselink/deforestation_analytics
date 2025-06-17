# rasterio
 
https://data.globalforestwatch.org/datasets/gfw::integrated-deforestation-alerts/about

Alerts can be downloaded in tiles as TIFFs from this [website](https://data.globalforestwatch.org/datasets/gfw::integrated-deforestation-alerts/explore?location=0.016316%2C20.448465%2C3.83)

[Integrated deforestation alerts](data.globalforestwatch.org)
Monitor forest disturbance alerts integrated from three satellite sources in near real time
There's information on the encoding in the Summary section if you click View Full Details on the left. They go back a few years but I'll just caution against using the alerts to analyze trends or quantify forest loss over time.

# How could I use Python code to derive a CSV with 4 fields: longitude, latitude, date, and confidence level from a raster which has the following encoding/syntax?:
# Each pixel (alert) encodes the date of disturbance and confidence level in one integer value. 
The leading integer of the decimal representation is:
- 2 for a low-confidence alert, 
- 3 for a high-confidence alert, and 
- 4 for an alert detected by multiple alert systems

The confidence integer [0] is followed by the number of days since December 31, 2014. For example:
- 20001 is a low confidence alert on January 1st, 2015
- 30055 is a high confidence alert on February 24, 2015
- 21847 is a low confidence alert on January 21, 2020
- 41847 is a highest confidence alert (detected by multiple alert systems) on January 21, 2020. Alert date represents the earliest detection
# 0 represents no alert / no-data value
