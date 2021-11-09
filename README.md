# Waste Transportation Sharing (WTS)

This repository contains code for Waste Transportation Sharing, a proposed solution for the GreenHack2021 hackathon. An application that optimizes waste management and transportation, and at the same time reduces traffic jams and CO2 generation. It can be used by transportation and waste management companies, and end-users such as companies and households.

## Prerequisites

The project was developed and tested on Ubuntu 19.10, with the following dependencies:

### Libraries

```
- numpy
- scipy
- pandas
- sklearn
- geopandas
- plotly
- dash
```

## Project Structure

The project is organized as follows:

    .
    ├── map_viz                 # Root directory for front-end logic
        ├── data                # Cached data used for front-end
        ├── src                 # Source code of front-end  
    ├── notebooks               # All Data Science and Machine Learning analyses, methods and data processing
    ├── LOCS.csv                # Geographic coordinates of our clusters
    ├── app.py                  # Main file that starts front-end


## Data

We used [public historic data of waste tracking in Slovenia](https://podatki.gov.si/dataset/9196eb56-430e-48f7-8399-cb4c799e5c2c/resource/98d26f77-3e35-41ad-9b9d-679a8d7f1068/download/izzivodpadkimodul1podatki.zip).

## Running the project

The project can be ran by executing `python3 maps/app.py` once the required libraries are isntalled.

## Authors

* Gorjan Popovski
* Bojan Evkoski
* Boshko Koloski
* Ljupche Milosheski
