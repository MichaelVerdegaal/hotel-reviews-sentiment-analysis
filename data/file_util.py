import os
import pickle

import dask.dataframe as dd

from config import KAGGLE_CSV, MANUAL_CSV, ROOT_DIR


def read_scraped_reviews():
    """
    Reads the pickled reviews file sourced from scraping
    :return: multidimensional list of reviews
    """
    filepath = os.path.join(ROOT_DIR, "static/reviews.pickle")
    return read_pickled_txt(filepath)


def read_kaggle_reviews():
    kaggle_df = dd.read_csv(KAGGLE_CSV)
    return kaggle_df


def read_manual_reviews():
    manual_df = dd.read_csv(MANUAL_CSV, delimiter=";;", engine="python", header=0)
    return manual_df


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
