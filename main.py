###
# This file will change frequently until all the modules have been written, for testing purposes
###
from data.dataframes import get_combined_review_df, preliminary_clean, clean_df_text, label_sentiment

d = get_combined_review_df()
e = preliminary_clean(d)
f = clean_df_text(e)
g = label_sentiment(f)
print(g)