###
# This file will change frequently until all the modules have been written, for testing purposes
###
import pandas as pd
import dask.dataframe as dd
from data.dataframes import get_all_review_sources, merge_dataframes

a, b, c = get_all_review_sources()

print(len(a))
print(len(b))
print(len(c))

# print(a.dtypes)
# print(b.dtypes)
# print(c.dtypes)

d = merge_dataframes(a, c)
print("\n\n")
print(len(d))
print(d.info())
print(d.columns)
