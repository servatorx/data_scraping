from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from pprint import pprint
from pymongo import MongoClient
driver = webdriver.Chrome()

## MVIDEO

driver.get("https://mvideo.ru")
time.sleep(4)
elems = driver.find_elements_by_xpath('//div[@class="gallery-layout sel-hits-block "]')[1]

button = elems.find_element_by_xpath('.//a[@class="next-btn sel-hits-button-next"]')
result = []
for i in range(4):

    for res in elems.find_elements_by_xpath('.//li[@class="gallery-list-item height-ready"]//a[@class="sel-product-tile-title"]'):
        if res.text != "":
            result.append(res.text)
    button.click()
    time.sleep(3)

pprint(result)


#exit(0)


## MAIL.ru письма

driver.get('https://mail.ru')
username = driver.find_element_by_id('mailbox:login')
username.send_keys('study.ai_172@mail.ru')
username.send_keys(Keys.RETURN)
time.sleep(1)
password = driver.find_element_by_id('mailbox:password')
password.send_keys('NextPassword172')
password.send_keys(Keys.RETURN)

time.sleep(3)

letters = driver.find_elements_by_class_name('llc')

links = []
i = 1
while True:
    time.sleep(1)
    letters = driver.find_elements_by_class_name('llc')
    if letters[-1].get_attribute('href') in links:
        print("Конец списка писем")
        break
    for letter in letters:
        if not letter.get_attribute('href') in links:
            links.append(letter.get_attribute('href'))
    actions = ActionChains(driver)
    actions.move_to_element(letters[-1])
    actions.perform()
    print(f"Обработано писем: {len(links)}")
    # i += 1
    # if i == 2:
    #     break

letters_info = []
for link in links:

    info = {}
    driver.get(link)
    time.sleep(3)
    info['contact'] = driver.find_element_by_class_name("letter-contact").text
    info['date'] = driver.find_element_by_class_name("letter__date").text
    info['text'] = driver.find_element_by_class_name("letter-body__body-content").text
    letters_info.append(info)
    driver.back()
    pprint(info)


pprint(letters_info)


client = MongoClient('127.0.0.1',27017)
db = client['users_db']

news_db = db.news
news_db.insert_many(letters_info)





