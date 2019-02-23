from selenium import webdriver
from taboola_box import TaboolaBox

def get_taboola_content(url):
    parsed_boxes = []
    browser = webdriver.Chrome()
    browser.get(url)
    taboola_content = browser.find_elements_by_xpath("//div[starts-with(@id, 'internal_trc_')]")
    for taboola_row in taboola_content:
        boxes = taboola_row.find_elements_by_xpath("//div[@data-item-title]")
        for box in boxes:
            text = box.text.split('\n')
            if len(text) >= 2:
                parsed_boxes.append(TaboolaBox(text[0], text[1]))
    return parsed_boxes

if __name__  == "__main__":
    url = "https://www.theblaze.com/news/tennessee-mom-carries-terminally-ill-baby-to-term"
    parsed_boxes = get_taboola_content(url)
    for box in parsed_boxes:
        print('Title: %s' % box.title)
        print('Sponsor: %s' % box.sponsor)
