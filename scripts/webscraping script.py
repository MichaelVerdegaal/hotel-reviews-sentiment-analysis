from data.scraping import get_all_catalog_urls, get_hotel_review_pages, get_reviews

if __name__ == '__main__':
    """
    This script runs all the webscraping functions to gather data from booking.com
    The script has a catalog url based in London by default, but this can be changed by providing a new one in 
    get_all_catalog_urls().
    """
    catalog_pages = get_all_catalog_urls()
    hotel_review_pages = get_hotel_review_pages()
    reviews = get_reviews()
