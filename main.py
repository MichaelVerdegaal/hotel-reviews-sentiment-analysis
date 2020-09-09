###
# This file will change frequently until all the modules have been written, for testing purposes
###
from data.scraping import *
import pandas as pd

c = gather_reviews()
print(c)

df = pd.DataFrame(c,
                  columns=["Hotel address", "Average Score", "Hotel name", "Nationality", "Negative review",
                           "Positive review", "Score"])
df.transpose()
df.to_pickle("./dfpickle.pkl")

print(df.head)
print(df.info())
