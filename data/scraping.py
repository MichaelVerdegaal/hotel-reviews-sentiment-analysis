import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# Searching for hotels on booking.com in London that have an average score
from data.file_util import write_pickled_txt, read_pickled_txt, file_exists, rootdir
import os

base_url = 'https://www.booking.com'
hotel_catalog_url = 'https://www.booking.com/searchresults.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaKkBiAEBmAExuAEKyAEF2AEB6AEB-AECiAIBqAIDuAL_4sP6BcACAdICJGFhY2JlMjA5LWE3ZWMtNGZhZC05MzI2LWM3NmRlMmQ2MGZiZNgCBeACAQ&sid=b7ae3ce18748b2e76e194075e2e4ae6c&tmpl=searchresults&ac_click_type=b&ac_position=1&class_interval=1&dest_id=222&dest_type=country&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&nflt=ht_id%3D204%3Bclass%3D5%3Bclass%3D4%3Bclass%3D3%3Bclass%3D2%3Bclass%3D1%3Buf%3D-2601889%3B&no_rooms=1&order=class_and_price&postcard=0&raw_dest_type=country&room1=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=0&slp_r_match=0&srpvid=7a84606916b6014e&ss=United%20Kingdom&ss_all=0&ss_raw=uni&ssb=empty&sshis=0&ssne=Spain&ssne_untouched=Spain&top_ufis=1&rows=25'


def get_html(page=hotel_catalog_url, headless_mode=True):
    """
    Gets the html content from a hotel catalog page
    :return: html as string
    """
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--lang=en_US')
    if headless_mode:
        # User agent needs to be set when headless mode is active, otherwise booking.com rejects the request
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.set_page_load_timeout(30)
    try:
        print(f"Retrieving web page for {page}")
        driver.get(page)
        time.sleep(2.5)
        return driver.page_source
    finally:
        driver.close()
        driver.quit()


def get_all_catalog_urls(catalog_url=hotel_catalog_url):
    """
    Scrapes all catalog pages from the base catalog page
    :return: list of urls
    """
    filepath = os.path.join(rootdir, "static/catalog_urls.pickle")
    if file_exists(filepath):
        return read_pickled_txt(filepath)
    else:
        print("Starting catalog page scraping!\n")
        print("-------------------------\n")
        base_html = get_html()
        base_soup = BeautifulSoup(base_html, 'lxml')
        page_list = [catalog_url]

        nextpage = base_soup.find('a', class_='paging-next')
        while nextpage:
            href = nextpage.get('href')
            new_page = f'{base_url}{href}'
            print(f"found new catalog page {new_page}")
            page_list.append(new_page)

            new_html = get_html(new_page)
            new_soup = BeautifulSoup(new_html, 'lxml')
            nextpage = new_soup.find('a', class_='paging-next')

        write_pickled_txt(page_list, filepath)
        print(f"Written catalog pages to {filepath}!")
        return page_list


def get_hotel_review_pages(catalog_url_list=get_all_catalog_urls()):
    """
    Scrapes all hotel review pages from a list of catalog pages.
    :param catalog_url_list: list of urls
    :return: list of urls
    """
    filepath = os.path.join(rootdir, "static/hotel_review_urls.pickle")
    if file_exists(filepath):
        return read_pickled_txt(filepath)
    else:
        print("Starting hotel review page scraping!")
        print("-------------------------\n")
        hotel_review_page_list = []
        for catalog_url in catalog_url_list:
            print(f"Scraping hotel links from {catalog_url}")
            catalog_html = get_html(catalog_url)
            catalog_soup = BeautifulSoup(catalog_html, 'lxml')
            hotel_page_list = catalog_soup.find_all('a', class_='hotel_name_link url')
            hotel_page_list = [i.get('href').replace("#hotelTmpl", "#tab-reviews") for i in hotel_page_list]
            hotel_page_list = [f"{base_url}{i}".replace("\n", "") for i in hotel_page_list]
            hotel_review_page_list.extend(hotel_page_list)

        write_pickled_txt(hotel_review_page_list, filepath)
        print(f"Written hotel review pages to {filepath}!")
        return hotel_review_page_list


def get_reviews(review_urls=get_hotel_review_pages()):
    """
    Scrapes review text from a hotel page (with the review tab open)
    :param review_urls: list of hotel page urls
    :return: list of reviews
    """
    filepath = os.path.join(rootdir, "static/reviews.pickle")
    if file_exists(filepath):
        return read_pickled_txt(filepath)
    else:
        print("Starting review scraping!\n")
        print("-------------------------\n")
        review_list = []
        for review_url in review_urls:
            print(f"Scraping reviews for page {review_url}")
            review_html = get_html(review_url)
            review_soup = BeautifulSoup(review_html, 'lxml')
            # Skip hotels with no average score, as this indicates they have no reviews
            if score_badge := review_soup.find("div", class_="bui-review-score__badge"):
                average_score = score_badge.text.strip()
                hotel_name = review_soup.find(id="hp_hotel_name_reviews").text.strip()
                hotel_address = review_soup.find("span", class_="hp_address_subtitle").text.strip()

                review_blocks = review_soup.select(".c-review-block")
                for r in review_blocks:
                    nationality = r.find("span", class_="bui-avatar-block__subtitle")
                    if nationality:
                        nationality = nationality.text.strip()
                    else:
                        nationality = "Nothing"
                    score = r.find(class_="bui-review-score__badge")
                    if score:
                        score = score.text.strip()
                    else:
                        score = "Nothing"
                    positive_review = r.find(class_="c-review__row")
                    if positive_review:
                        positive_review = positive_review.p.find(class_="c-review__body").text.strip()
                    else:
                        positive_review = "Nothing"
                    negative_review = r.find(class_="lalala")
                    if negative_review:
                        negative_review = negative_review.p.find(class_="c-review__body").text.strip()
                    else:
                        negative_review = "Nothing"
                    review = [hotel_address, average_score, hotel_name, nationality, negative_review, positive_review,
                              score]
                    print(f'Adding review for hotel "{hotel_name}"')
                    review_list.append(review)
        write_pickled_txt(review_list, filepath)
        print(f"Written reviews to {filepath}!")
        return review_list
