###
# This file will change frequently until all the modules have been written, for testing purposes
###
import pandas as pd

from data.scraping import get_reviews

c = get_reviews()

df = pd.DataFrame(c,
                  columns=["Hotel address", "Average Score", "Hotel name", "Nationality", "Negative review",
                           "Positive review", "Score"])
df.transpose()

print(df.head)
print(df.info())
