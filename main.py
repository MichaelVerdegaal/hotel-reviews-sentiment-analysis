###
# This file will change frequently until all the modules have been written, for testing purposes
###
from data.scraping import *

p = get_all_catalog_urls()
c = get_hotel_review_pages(p)
