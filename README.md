# Share Your Garbage

This repository contains code for Share Your Garbage, an application that optimizes waste management and transportation, and at the same time reduces traffic jams and CO2 generation. Our application can be used  by transportation and waste management companies, and end-users such as companies and households.

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
```

## Project Structure

The project is organized as follows:

    .
    ├── maps                        # Root directory for front-end
        ├── map_viz                 # Root directory for front-end logic
            ├── data                # Cached data used for front-end
            ├── src                 # Source code of front-end  
        ├── LOCS.csv                # Geographic coordinates of our clusters
        ├── app.py                  # Main file that starts front-end
    ├── exploratory_analysis.ipynb  # A notebook used for exploratory analysis and clustering waste categories into a few similar groups
    ├── GeoGether.ipynb             # A notebook that resolves addresses to geographic coordinates


## Data

We used [public historic data of waste tracking in Slovenia](https://podatki.gov.si/dataset/9196eb56-430e-48f7-8399-cb4c799e5c2c/resource/98d26f77-3e35-41ad-9b9d-679a8d7f1068/download/izzivodpadkimodul1podatki.zip).

## Running the project

The project can be ran by executing `python3 maps/app.py` once the required libraries are isntalled.

## Authors

* Gorjan Popovski
* Bojan Evkovski
* Boshko Koloski
* Ljupche Milosheski
