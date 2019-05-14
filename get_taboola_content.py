from bs4 import BeautifulSoup
from selenium import webdriver
from taboola_box import TaboolaBox
import os
import re
import requests
import csv
import time
import signal
from contextlib import contextmanager


@contextmanager
def timeout(time):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    raise TimeoutError

CSV_FOLDER = 'websites/'
DATA_FOLDER = 'data/'
URL_IN_EXCEPTIONS = ['news']

'''
Create a regex representing the string of the article URl.
'''
def _get_regex_from_pattern(pattern):
    pattern = pattern.replace('///', '.*/')
    pattern = pattern.replace('4y','[0-9]{4}')
    pattern = pattern.replace('2m','[0-9]{2}')
    pattern = pattern.replace('2d','[0-9]{2}')
    pattern = pattern.replace('2y','[0-9]{2}')
    pattern = pattern.replace('headline','.*')
    pattern = pattern.replace('section','[a-zA-Z]+')
    pattern = pattern.replace('?','\?')
    return pattern

'''
Get the links of all articles on a website that fit a given
pattern for URLs of news articles.
Returns: list of article links if they are found; empty list otherwise.
'''
def get_article_links(site, stripped_url, pattern):
    links = []
    try:
        page = requests.get(site)
        soup = BeautifulSoup(page.text, "html.parser")
        pattern = re.compile(_get_regex_from_pattern(pattern))
        for link in soup.find_all('a', href=True):
            # Get the components of the URL.
            url_components = link['href'].split('/')
            start = 0
            for i in range(len(url_components)):
                if stripped_url in url_components[i] or url_components[i] in stripped_url \
                and url_components[i] != '' and url_components[i] not in URL_IN_EXCEPTIONS:
                    start = i
            url_pattern = '/' + ('/').join(url_components[start+1:])
            # print(url_pattern)
            if pattern.match(url_pattern):
                links.append(url_pattern)
        return links
    except:
        return []

'''
Get Taboola content from a page with Taboola advertisements.
Returns: TaboolaBox objects if boxes are found; empty array otherwise.
'''
def get_taboola_content(driver, url):
    parsed_boxes = []
    try:
        print('Scraping data from %s...' % url)
        driver.get(url)
        taboola_content = driver.find_elements_by_xpath("//div[starts-with(@id, 'internal_trc_')]")
        for taboola_row in taboola_content:
            boxes = taboola_row.find_elements_by_xpath("//div[@data-item-title]")
            for box in boxes:
                link = box.find_element_by_css_selector('a').get_attribute("href")
                text = box.text.split('\n')
                if len(text) >= 2:
                    parsed_boxes.append(TaboolaBox(text[0], text[1], link, url))
        return parsed_boxes
    except:
        return parsed_boxes

if __name__  == "__main__":
    driver = webdriver.Chrome() # create a webdriver.
    driver.set_page_load_timeout(20)

    for filename in os.listdir(CSV_FOLDER):
        # Iterate through CSVs with data.
        if filename.endswith('.csv'):
            with open(CSV_FOLDER + filename, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    if row[3] == 'TRUE' and row[5]: # Taboola website.
                        # Get the article links.
                        big_url = 'https://www.' + row[0]
                        article_links = get_article_links(big_url, row[0], row[5])
                        if len(article_links) == 0:
                            big_url = 'http://www.' + row[0]
                            if len(get_article_links(big_url, row[0], row[5])) == 0:
                                print('Could not scrape data for %s' % row[0])
                        # Scrape the Taboola ads.
                        article_links = list(set(article_links))
                        publisher = row[0]
                        if not os.path.isdir('data/%s' % publisher):
                            os.mkdir('data/%s' % publisher)

                        for link_end in article_links:
                            url = big_url + link_end
                            parsed_boxes = get_taboola_content(driver, url)
                            for box in parsed_boxes:
                                 box.write(publisher)
    driver.quit()
