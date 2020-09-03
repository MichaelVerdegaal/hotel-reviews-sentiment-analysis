import pandas as pd

kaggle_csv = "../static/kaggle_reviews.csv"
# TODO: vul path in wanneer het bestand bestaat
manual_csv = ""


def csv_to_df(filepath):
    return pd.DataFrame(pd.read_csv(filepath))


def read_kaggle():
    return csv_to_df(kaggle_csv)