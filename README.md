# model_data_to_netCDF

Project made to download oceanic data from  http://dd.meteo.gc.ca/model_gem_regional/coupled/gulf_st-lawrence . The source data are in .grib2, but this project allows to convert them in NetCDF following the CF-1.8.

## Installation

Along with the project, the following libraries need to be installed:

* pygrib
    ```
    conda install -c conda-forge pygrib
    ```
* netCDF4
    ```
  pip install netCDF4
  ```
* requests
    ```
    pip install request
    ```

## Get started

In the terminal, navigate to the directory of the project. 
Then, you can download the data available with this line:
```
python __main__.py load_grib
```
This line of code will create a folder called "grib" (if not already existing) and will inject the .grib2 data in it. 


In order to convert grib files to nc, you have to use:
```
python __main__.py convert_to_nc
```
It will first create a "nc" folder (if not already existing).
It will then convert to NetCDF all the .grib2 files in the "grib" folder that are note already converted (not present in the "nc" folder. 
