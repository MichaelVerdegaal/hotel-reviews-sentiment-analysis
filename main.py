###
# This file will change frequently until all the modules have been written, for testing purposes
###
import pandas as pd
import dask.dataframe as dd
from data.dataframes import get_combined_review_df, clean_df


d = get_combined_review_df()
c = clean_df(d)
l = c.tail(n=20)
print(l)