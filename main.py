###
# This file will change frequently until all the modules have been written, for testing purposes
###
from data.scraping import *

c = get_hotel_review_pages()
print(len(c))