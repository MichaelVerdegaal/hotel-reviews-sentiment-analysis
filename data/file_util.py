import dask.dataframe as dd

kaggle_csv = "static/kaggle_reviews.csv"
# TODO: vul path in wanneer het bestand bestaat
manual_csv = ""


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
