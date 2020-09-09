import os
from pathlib import Path
import pickle

import dask.dataframe as dd

kaggle_csv = "static/kaggle_reviews.csv"
manual_csv = "static/manual_reviews.csv"
rootdir = Path(os.getcwd()).parents[0]


def csv_to_df(filepath):
    """
    Reads a csv and converts it to a dataframe
    :param filepath: path to csv file
    :return: dask dataframe
    """
    return dd.read_csv(filepath)


def read_all_csv():
    """
    Master function to read all csv files
    :return: pandas dataframes
    """
    kaggle_df = csv_to_df(kaggle_csv)
    return kaggle_df


def write_pickled_txt(object_to_dump, filepath):
    """
    Pickled and writes an object to a file as long as the file doesn't exist
    :param object_to_dump: object that will be written
    :param filepath: where the file is
    """
    if file_exists(filepath):
        pass
    else:
        with open(filepath, 'wb') as f:
            pickle.dump(object_to_dump, f)


def read_pickled_txt(filepath):
    """
    Reads from a file and unpickles the stored object
    :param filepath: where the file is
    :return: unpickled object
    """
    with open(filepath, 'rb') as f:
        try:
            unpickled_object = pickle.load(f)
            return unpickled_object
        except pickle.UnpicklingError as e:
            raise e


def file_exists(filepath):
    """
    Check if a file exists
    :param filepath: filepath as string
    :return: boolean
    """
    return os.path.isfile(filepath)
