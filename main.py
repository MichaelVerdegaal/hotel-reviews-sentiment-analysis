###
# This file will change frequently until all the modules have been written, for testing purposes
###
from data.file_util import read_labeled_reviews
from data.database import *

# review_df = read_labeled_reviews()
c = db_to_df(40)
print(c.columns)