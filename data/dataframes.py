import dask.dataframe as dd
import pandas as pd

from data.file_util import read_scraped_reviews, read_kaggle_reviews, read_manual_reviews

usable_column_list = ["Hotel_Address", "Average_Score", "Hotel_Name", "Reviewer_Nationality", "Negative_Review",
                      "Positive_Review", "Reviewer_Score"]


def process_scraped_reviews(reviews=read_scraped_reviews()):
    """
    Processes the scraped reviews so it can be successfully merged
    :param reviews: multi dimensional list of reviews
    :return: dataframe
    """
    df = pd.DataFrame(reviews, columns=usable_column_list)
    df.transpose()
    df = dd.from_pandas(df, npartitions=3)
    df['Average_Score'] = df['Average_Score'].astype('float64')
    df['Reviewer_Score'] = df['Reviewer_Score'].astype('float64')
    return df


def merge_dataframes(df1, df2):
    """
    Merges two dataframes together
    :param df1: first dataframe
    :param df2: second dataframe
    :return: merged dataframe
    """
    new_df = dd.merge(df1[usable_column_list],
                      df2[usable_column_list],
                      on=usable_column_list,
                      how='outer')
    return new_df


def get_all_review_sources():
    """
    Master function to get all available dataframes from their respective sources
    :return: 3 dataframes
    """
    kaggle_df = read_kaggle_reviews()[usable_column_list]
    manual_df = read_manual_reviews()
    scraped_df = process_scraped_reviews()
    return kaggle_df, manual_df, scraped_df


def get_combined_review_df():
    """
    Executes all other functions in this file to return 1 dataframe filled with reviews
    :return: dataframe
    """
    kaggle_df, manual_df, scraped_df = get_all_review_sources()
    final_df = merge_dataframes(kaggle_df, manual_df)
    final_df = merge_dataframes(final_df, scraped_df)
    return final_df
