import os
import pickle

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Searching for hotels on booking.com in London that have an average score
base_url = 'https://www.booking.com'
hotel_catalog_url = 'https://www.booking.com/searchresults.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaKkBiAEBmAExuAEKyAEF2AEB6AEB-AECiAIBqAIDuAL_4sP6BcACAdICJGFhY2JlMjA5LWE3ZWMtNGZhZC05MzI2LWM3NmRlMmQ2MGZiZNgCBeACAQ&sid=b7ae3ce18748b2e76e194075e2e4ae6c&tmpl=searchresults&ac_click_type=b&ac_position=1&class_interval=1&dest_id=222&dest_type=country&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&nflt=ht_id%3D204%3Bclass%3D5%3Bclass%3D4%3Bclass%3D3%3Bclass%3D2%3Bclass%3D1%3Buf%3D-2601889%3B&no_rooms=1&order=class_and_price&postcard=0&raw_dest_type=country&room1=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=0&slp_r_match=0&srpvid=7a84606916b6014e&ss=United%20Kingdom&ss_all=0&ss_raw=uni&ssb=empty&sshis=0&ssne=Spain&ssne_untouched=Spain&top_ufis=1&rows=25'


def file_exists(filepath):
    """
    Check if a file exists
    :param filepath: filepath as string
    :return: boolean
    """
    return os.path.isfile(filepath)


def write_pickled_txt(object_to_dump, filepath):
    """
    Pickled and writes an object to a file as long as the file doesn't exist
    :param object_to_dump: object that will be written
    :param filepath: where the file is
    """
    if file_exists(filepath):
        pass
    else:
        outfile = open(filepath, 'wb')
        pickle.dump(object_to_dump, outfile)
        outfile.close()


def read_pickled_txt(filepath):
    """
    Reads from a file and unpickles the stored object
    :param filepath: where the file is
    :return: unpickled object
    """
    infile = open(filepath, 'rb')
    unpickled_object = pickle.load(infile)
    infile.close()
    return unpickled_object


def get_html(page=hotel_catalog_url):
    """
    Gets the html content from a hotel catalog page
    :return: html as string
    """
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(page)
    driver.implicitly_wait(4)
    try:
        return driver.page_source
    finally:
        driver.close()
        driver.quit()


def get_all_catalog_urls():
    """
    Scrapes all catalog pages from the base catalog page
    :return: list of urls
    """
    filepath = "static/catalog_urls.txt"
    if file_exists(filepath):
        return read_pickled_txt(filepath)
    else:
        base_html = get_html()
        base_soup = BeautifulSoup(base_html, 'lxml')
        page_list = [hotel_catalog_url]

        nextpage = base_soup.find('a', class_='paging-next')
        while nextpage:
            href = nextpage.get('href')
            new_page = f'{base_url}{href}'
            page_list.append(new_page)

            new_html = get_html(new_page)
            new_soup = BeautifulSoup(new_html, 'lxml')
            nextpage = new_soup.find('a', class_='paging-next')

        write_pickled_txt(page_list, filepath)
        return page_list


def get_hotel_review_pages(catalog_url_list=get_all_catalog_urls()):
    """
    Scrapes all hotel review pages from a list of catalog pages.
    :param catalog_url_list: list of urls
    :return: list of urls
    """
    filepath = "static/hotel_review_urls.txt"
    if file_exists(filepath):
        return read_pickled_txt(filepath)
    else:
        hotel_review_page_list = []
        for catalog_url in catalog_url_list:
            catalog_html = get_html(catalog_url)
            catalog_soup = BeautifulSoup(catalog_html, 'lxml')
            hotel_page_list = catalog_soup.find_all('a', class_='hotel_name_link url')
            hotel_page_list = [i.get('href').replace("#hotelTmpl", "#tab-reviews") for i in hotel_page_list]
            hotel_page_list = [f"{base_url}{i}".replace("\n", "") for i in hotel_page_list]
            hotel_review_page_list.extend(hotel_page_list)

        write_pickled_txt(hotel_review_page_list, filepath)
        return hotel_review_page_list
