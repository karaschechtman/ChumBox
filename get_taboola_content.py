from selenium import webdriver
from taboola_box import TaboolaBox
import os
import requests
from bs4 import BeautifulSoup
import re

def _get_regex_from_pattern(pattern):
    pattern = pattern.replace('///', '.*/')
    pattern = pattern.replace('4y','[0-9]{4}')
    pattern = pattern.replace('2m','[0-9]{2}')
    pattern = pattern.replace('2d','[0-9]{2}')
    pattern = pattern.replace('2y','[0-9]{2}')
    pattern = pattern.replace('headline','.*')
    print(pattern)
    return pattern

'''
Get the links of all articles on a website that fit a given
pattern for URLs of news articles.
'''
def get_article_links(site, stripped_url, pattern):
    print(pattern)
    page = requests.get(site)
    soup = BeautifulSoup(page.text, "html.parser")
    pattern = re.compile(_get_regex_from_pattern(pattern))
    for link in soup.find_all('a', href=True):
        # Get the components of the URL.
        url_components = link['href'].split('/')
        start = 0
        for i in range(len(url_components)):
            if stripped_url in url_components[i] or url_components[i] in stripped_url:
                start = i
        url_pattern = ('/').join(url_components[start+1:])
        if pattern.match(url_pattern):
            print(url_pattern)

'''
Get Taboola content from a page with Taboola advertisements.
'''
def get_taboola_content(driver, url):
    parsed_boxes = []
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


if __name__  == "__main__":
    get_article_links('https://www.chron.com/', 'chron.com', '///article/headline')
    # driver = webdriver.Chrome()
    # publisher = 'FoxNews'
    # if not os.path.isdir('data/%s' % publisher):
    #     os.mkdir('data/%s' % publisher)
    # url = "https://www.foxnews.com/us/nj-student-dies-after-prom"
    # parsed_boxes = get_taboola_content(driver, url)
    # for box in parsed_boxes:
    #     box.write(publisher)
    #
    # publisher = 'FoxNews'
    # if not os.path.isdir('data/%s' % publisher):
    #     os.mkdir('data/%s' % publisher)
    # url = "https://www.foxnews.com/world/iranian-president-aide-trump-war-mustache-john-bolton"
    # parsed_boxes = get_taboola_content(driver, url)
    # for box in parsed_boxes:
    #     box.write(publisher)
    #
    # driver.quit()
