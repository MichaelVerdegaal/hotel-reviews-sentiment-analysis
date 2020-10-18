###
# This file will change frequently until all the modules have been written, for testing purposes
###
import pandas as pd
from data.dataframes import get_combined_review_df, preliminary_clean, preprocess_clean
from data.file_util import read_clean_reviews


a = get_combined_review_df()

b = preliminary_clean(a)
c = preprocess_clean(b)

d = read_clean_reviews()
print(d)