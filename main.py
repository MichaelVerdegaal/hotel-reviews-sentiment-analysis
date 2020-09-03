import pandas as pd

df = pd.DataFrame(pd.read_csv("static/kaggle_reviews.csv"))
df = df.sort_values(by=['Review_Date', 'Average_Score'])

print(df.head())
print(df.info())
print(df.head())
print(df.head())