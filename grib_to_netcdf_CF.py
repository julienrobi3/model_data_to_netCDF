import pygrib
from netCDF4 import Dataset
from datetime import datetime
import os
import pathlib


class NetCDFFile:
    def __init__(self):
        self.basepath = str(pathlib.Path(__file__).parent.absolute())
        self.basepath_grib = self.basepath + "\\grib\\"
        self.basepath_nc = self.basepath + "\\nc\\"
        self.grib_folders = os.listdir(self.basepath_grib)
        self.nc_files = self.list_nc()

    def list_nc(self):
        if not os.path.isdir(self.basepath_nc):
            return []
        else:
            nc_with_extension = os.listdir(self.basepath_nc)
            nc_files = []
            for file in nc_with_extension:
                nc_files.append(os.path.splitext(file)[0])
            return nc_files

    def grib_to_delete(self):
        return set(self.nc_files).intersection(self.grib_folders)

    def grib_to_convert(self):
        return set(self.grib_folders) - set(self.nc_files)

    def create_netcdf_from_grib(self):
        gribs_to_convert = self.grib_to_convert()
        for grib in gribs_to_convert:
            need_to_create = True
            directory = self.basepath_nc
            if not os.path.isdir(directory):
                os.makedirs(directory)
            nc_file_path = self.basepath_nc + grib + '.nc'
            f = Dataset(nc_file_path, 'w', format='NETCDF4')
            list_files = os.listdir(self.basepath_grib + grib)
            index = 0
            while need_to_create:
                if list_files[index].endswith(".grib2"):
                    file = list_files[index]
                    variables = pygrib.open(self.basepath_grib+grib+"\\"+file)
                    variable = variables.read()

                    # on va chercher lon et lat et le temps d'émission de la prédiction à partir de la première variable
                    lats, lons = variable[0].latlons()
                    date = datetime(variable[0]["year"], variable[0]["month"], variable[0]["day"], variable[0]["hour"],
                                    0, 0)

                    f.description = "Description text"
                    f.history = "Created from .grib2 file on " + datetime.today().strftime("%d/%m/%y")
                    f.institution = variable[0]["centreDescription"]

                    f.createDimension('time', None)
                    f.createDimension('lat', lats.shape[0])
                    f.createDimension('lon', lons.shape[1])

                    longitude = f.createVariable('lon', 'f4', 'lon')
                    longitude.units = 'degrees_east'
                    longitude.long_name = "longitude"
                    longitude.standard_name = "longitude"
                    longitude[:] = lons[0]

                    latitude = f.createVariable('lat', 'f4', 'lat')
                    latitude.units = 'degrees_north'
                    latitude.long_name = "latitude"
                    latitude.standard_name = "latitude"
                    latitude[:] = [i[0] for i in lats]

                    time = f.createVariable('time', 'd', 'time')
                    time.units = "hours since " + str(date)
                    time.long_name = "time"
                    time.standard_name = "time"

                    for data in variable:
                        if data["name"] != "unknown":
                            var = f.createVariable(data["shortName"], 'f4', ("time", 'lat', "lon"))
                            var.units = data["units"]
                            var.long_name = data["name"]
                            var.standard_name = data["cfName"]

                    need_to_create = False

            i = 0
            for fi in list_files:
                if fi.endswith(".grib2"):
                    variables = pygrib.open(self.basepath_grib + grib + "/" + fi)
                    variable = variables.read()
                    f["time"][i] = variable[0]["forecastTime"]

                    for data in variable:
                        if data["name"] != "unknown":
                            var_name = data["shortName"]
                            f[var_name][i, :, :] = data["values"]
                    i += 1


if __name__ == "__main__":
    filen_folder = 'CMC_coupled-rdps-stlawrence-ocean_latlon0.02x0.03_2020121000'
    netcdf_file = NetCDFFile()
    print(netcdf_file.grib_to_delete())
    print(netcdf_file.grib_to_convert())
    netcdf_file.create_netcdf_from_grib()



