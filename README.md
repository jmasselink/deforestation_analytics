# Deforestation Analytics

This repo contains scripts to calculate deforestation using two different datasets:
1. Global Forest Watch Integrated Disturbance Alerts (formerly Integrated Deforestation Alerts)
>  https://data.globalforestwatch.org/datasets/gfw::integrated-deforestation-alerts/about

- Alerts can be downloaded in tiles as TIFFs from this [website](https://data.globalforestwatch.org/datasets/gfw::integrated-deforestation-alerts/explore?location=0.016316%2C20.448465%2C3.83)

 [Integrated Disturbance alerts](data.globalforestwatch.org)
- Monitor forest disturbance alerts integrated from four satellite sources in near real time.  

There's information on the encoding in the Summary section if you click View Full Details on the left. They go back a few years but I'll just caution against using the alerts to analyze trends or quantify forest loss over time.  

2. Global Forest Change 2000-2025
> https://storage.googleapis.com/earthenginepartners-hansen/GFC-2025-v1.13/download.html

Download 10 DD x 10 DD grid, using the 
`lossyear` dataset.

---
### Environment setup

Using Conda:
`conda env create -f environment.yml`
