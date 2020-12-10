import sys
from grib_to_netcdf_CF import NetCDFFile
from drftgribharvestor import GribHarvestor

if __name__ == '__main__':

    if sys.argv[1] == "load_grib":
        grib = GribHarvestor()
        grib.load_grib()
    if sys.argv[1] == "convert_to_nc":
        netcdf_file = NetCDFFile()
        netcdf_file.create_netcdf_from_grib()
