import glob
import pandas as pd


def return_shp_path_from_folder(folder_path):

    extention = '.shp'

    search_format = '{}{}{}{}'.format(folder_path,'/**/', '*', extention)

    return glob.glob(search_format, recursive=True)


def save_pandas_csv(dataframe, file_name):

    path = "../vector/result/"
    file_name = file_name
    extention = ".csv"

    full_path = "{}{}{}".format(path, file_name, extention)

    dataframe.to_csv(full_path, sep=",")
