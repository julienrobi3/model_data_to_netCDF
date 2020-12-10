"""
Code de téléchargement de fichier grib de données de prévision provenant d'ECCC
"""


import requests
import shutil
import os.path
import datetime
import pathlib

# example : http://dd.meteo.gc.ca/model_gem_regional/coupled/gulf_st-lawrence/grib2/00/001/CMC_coupled-rdps-stlawrence-ocean_latlon0.02x0.03_2019010300_P001.grib2
# example : http://dd.meteo.gc.ca/model_gem_regional/coupled/gulf_st-lawrence/grib2/00/001/CMC_coupled-rdps-stlawrence-atmosphere_latlon0.02x0.03_2019010300_P001.grib2


class GribHarvestor:
    def __init__(self):
        self.coupledbaspath = 'https://dd.meteo.gc.ca/model_gem_regional/coupled/gulf_st-lawrence/grib2/'
        self.current_path = str(pathlib.Path(__file__).parent.absolute())

    def load_grib(self):
        print('Telechargement des donnees d''aujourd''hui de prevision utilisees par le moteur de derive')
        dnow = datetime.datetime.now()
        print('' + dnow.strftime('%Y%m%d-%H:%M:%S'))
        # dforecast = datetime.datetime(dnow.year, dnow.month, dnow.day, 0, 0, 0)
        dforecast = datetime.datetime(dnow.year, dnow.month, dnow.day, 0, 0, 0) + datetime.timedelta(hours=-24)
        # genere le nom du fichier
        # pour les heures aujourdui et demain
        for daystocheck in range(0, 2):
            print('Jour:' + str(daystocheck))
            for hoursgen in range(0, 24, 6):
                local_directory = self.create_directory(dforecast, hoursgen)
                for h in range(1, 49):
                    # atmosfilename = generateFileName(True, dforecast, hoursgen, h)
                    stlawfilename = self.generate_file_name(dforecast, hoursgen, h)
                    # atmoslocal = generatelocalpath( atmosfilename, hoursgen, h)
                    tlawlocal = local_directory + "/" + stlawfilename
                    # verifie s'il existe localement
                    # if not isFileLocal(atmoslocal):
                    #     # si non, essaie de telecharger
                    #     downloadpath = generatePethToFile(True, hoursgen, dforecast, h)
                    #     tryDownloadGrib(downloadpath, atmoslocal)
                    if not self.is_file_local(tlawlocal):
                        # si non, essaie de telecharger
                        downloadpath = self.generate_path_to_file(hoursgen, dforecast, h)
                        self.try_download_grib(downloadpath, tlawlocal)
                if len(os.listdir(local_directory)) == 0:
                    os.rmdir(local_directory)

            dforecast = dforecast + datetime.timedelta(hours=24)

    def create_directory(self, dforecast, hoursgen):
        directory_name = 'CMC_coupled-rdps-stlawrence-ocean_latlon0.02x0.03_' + dforecast.strftime(
            '%Y%m%d') + str(
            hoursgen).rjust(2, '0')
        directory = self.current_path + "/grib/" + directory_name
        if not os.path.isdir(directory):
            os.makedirs(directory)
        return directory

    @staticmethod
    def generate_file_name(prevdate, hoursgenerated, hoursforecast):
        filename = 'CMC_coupled-rdps-stlawrence-ocean_latlon0.02x0.03_'
        # filedatetime = '2019010300_P001'
        filedatetime = prevdate.strftime('%Y%m%d') + str(hoursgenerated).rjust(2, '0') + '_P' + str(
            hoursforecast).rjust(3, '0')
        retfilename = filename + filedatetime + '.grib2'
        return retfilename

    @staticmethod
    def is_file_local(filepath):
        """
        Regarde si le ficheir exist localement dans le bon repertoire
        :param filepath:
        :return:
        """
        return os.path.isfile(filepath)

    def generate_path_to_file(self, hoursgenerated, prevdate, hoursforecast):
        retpath = self.coupledbaspath
        if hoursgenerated in [0, 6, 12, 18]:
            retpath += str(hoursgenerated).rjust(2, '0') + '/'
        else:
            raise ValueError('hoursgenerated out of scope')
        hoursofday = str(hoursforecast).rjust(3, '0') + '/'
        filename = 'CMC_coupled-rdps-stlawrence-ocean_latlon0.02x0.03_'

        filedatetime = prevdate.strftime('%Y%m%d') + str(hoursgenerated).rjust(2, '0') + '_P' + str(
            hoursforecast).rjust(3, '0')
        retpath += hoursofday + filename + filedatetime + '.grib2'
        return retpath

    @staticmethod
    def try_download_grib(filepath, destpath):
        r = requests.head(filepath)
        if r.status_code == requests.codes.ok:
            print('dwonloading ' + filepath)
            response = requests.get(filepath, stream=True)
            with open(destpath, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response


if __name__ == "__main__":
    grib = GribHarvestor()
    grib.load_grib()