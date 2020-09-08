###
# This file will change frequently until all the modules have been written, for testing purposes
###
from data.scraping import *

c = gather_reviews()

for i in c:
    print(i)
