import os
import re

import dask.dataframe as dd
import nltk
import pandas as pd
from langdetect import detect
from nltk.stem import WordNetLemmatizer, PorterStemmer

from config import ROOT_DIR
from data.file_util import read_scraped_reviews, read_kaggle_reviews, read_manual_reviews, file_exists, \
    read_pickled_txt, write_pickled_txt


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
    final_df.repartition(npartitions=3)
    return final_df


def clean_df(df):
    def is_en(text):
        try:
            if text == "" or text is None:
                return False
            langcode = detect(text)
            # Portugal code is included because it incorrectly detects some english text as portuguese
            return langcode in ['en', 'ca', 'pt']
        except:
            return False

    def pre_process_text(text):
        # clean (convert to lowercase, remove punctuations and unneeded characters, then strip)
        text = re.sub(r'[^\w\s]', '', str(text).lower().strip())

        # Tokenize (convert from string to list)
        lst_text = text.split()
        # remove Stopwords
        lst_text = [word for word in lst_text if word not in lst_stopwords]

        # Lemmatisation (convert the word into root word)
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]

        # back to string from list
        text = " ".join(lst_text)
        return text

    filepath = os.path.join(ROOT_DIR, "static/clean_df.pickle")
    if file_exists(filepath):
        return read_pickled_txt(filepath)
    else:
        print("\nDownloading nltk libraries...")
        nltk.download('stopwords')
        nltk.download('wordnet')
        lst_stopwords = nltk.corpus.stopwords.words("english")

        print("\nMerging columns...")
        df['Review'] = df['Positive_Review'] + ' ' + df['Negative_Review']
        df = df.drop('Positive_Review', 1)
        df = df.drop('Negative_Review', 1)

        print("\nRemoving non-english reviews...")
        df = df[df['Review'].apply(lambda x: is_en(x))]

        print("\nPre-processing text...")
        df['Review'] = df['Review'].apply(pre_process_text)

        write_pickled_txt(df, filepath)
        print(f"\nWritten reviews to {filepath}!")
        return df
