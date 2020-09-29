###
# This file will change frequently until all the modules have been written, for testing purposes
###
import pandas as pd
import dask.dataframe as dd
from data.dataframes import get_combined_review_df, clean_df
from data.file_util import read_clean_reviews


d = get_combined_review_df()
d = d.tail(n=5000000)

c = clean_df(d)

e = read_clean_reviews()
print(e)