from selenium import webdriver
from taboola_box import TaboolaBox
import os

def get_taboola_content(url):
    parsed_boxes = []
    browser = webdriver.Chrome()
    browser.get(url)
    taboola_content = browser.find_elements_by_xpath("//div[starts-with(@id, 'internal_trc_')]")
    for taboola_row in taboola_content:
        boxes = taboola_row.find_elements_by_xpath("//div[@data-item-title]")
        for box in boxes:
            link = box.find_element_by_css_selector('a').get_attribute("href")
            text = box.text.split('\n')
            if len(text) >= 2:
                parsed_boxes.append(TaboolaBox(text[0], text[1], link, url))
    return parsed_boxes

if __name__  == "__main__":
    # publisher = 'TheBlaze'
    # if not os.path.isdir('data/%s' % publisher):
    #     os.mkdir('data/%s' % publisher)
    # url = "https://www.theblaze.com/news/tennessee-mom-carries-terminally-ill-baby-to-term"
    # parsed_boxes = get_taboola_content(url)
    # for box in parsed_boxes:
    #     box.write(publisher)

    publisher = 'FoxNews'
    if not os.path.isdir('data/%s' % publisher):
        os.mkdir('data/%s' % publisher)
    url = "https://www.foxnews.com/world/iranian-president-aide-trump-war-mustache-john-bolton"
    parsed_boxes = get_taboola_content(url)
    for box in parsed_boxes:
        box.write(publisher)
