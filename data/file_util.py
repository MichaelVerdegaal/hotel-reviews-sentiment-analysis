import pickle

import pandas as pd

from config import *


def pickle_object(object_to_dump, filepath):
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


def pickle_dataframe(dataframe, filepath):
    """
    Pickled and writes an object to a file as long as the file doesn't exist
    :param object_to_dump: object that will be written
    :param filepath: where the file is
    """
    if file_exists(filepath):
        pass
    else:
        dataframe.to_pickle(filepath)


def read_pickled_dataframe(filepath):
    return pd.read_pickle(filepath)


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


def read_scraped_reviews():
    """
    Reads the pickled reviews file sourced from scraping
    :return: multidimensional list of reviews
    """
    filepath = os.path.join(ROOT_DIR, "static/scraped_reviews.pickle")
    return read_pickled_txt(filepath)


def read_kaggle_reviews():
    kaggle_df = pd.read_csv(KAGGLE_CSV)
    return kaggle_df


def read_manual_reviews():
    manual_df = pd.read_csv(MANUAL_CSV, delimiter=";;", engine="python", header=0)
    return manual_df


def read_precleaned_reviews():
    filepath = os.path.join(ROOT_DIR, PRELIMINARY_CLEAN_DF)
    return read_pickled_dataframe(filepath)


def read_clean_reviews():
    filepath = os.path.join(ROOT_DIR, CLEAN_DF)
    return read_pickled_dataframe(filepath)


def read_labeled_reviews():
    filepath = os.path.join(ROOT_DIR, LABELED_DF)
    return read_pickled_dataframe(filepath)
