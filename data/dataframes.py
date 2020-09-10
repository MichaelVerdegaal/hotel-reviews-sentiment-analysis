import dask.dataframe as dd
import pandas as pd

from data.file_util import read_all_csv, read_scraped_reviews


def multidim_list_to_df(my_list):
    """
    Convers a multidimensional list to a dataframe
    :param my_list: multidimensional list (make sure the amount of columns are correct)
    :return: dask dataframe
    """
    df = pd.DataFrame(my_list,
                      columns=["Hotel_Address", "Average_Score", "Hotel_Name", "Reviewer_Nationality",
                               "Negative_Review", "Positive_Review", "Reviewer_Score"])
    df.transpose()
    return dd.from_pandas(df, npartitions=3)


def get_all_review_sources():
    """
    Master function to get all available dataframes from their respective sources
    :return: 3 dataframes
    """
    kaggle_df, manual_df = read_all_csv()
    scraped_df = multidim_list_to_df(read_scraped_reviews())
    return kaggle_df, manual_df, scraped_df
