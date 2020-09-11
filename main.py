###
# This file will change frequently until all the modules have been written, for testing purposes
###
import pandas as pd
import dask.dataframe as dd
from data.dataframes import get_combined_review_df


d = get_combined_review_df()
c = d.npartitions
print("\n\n")
print(c)
