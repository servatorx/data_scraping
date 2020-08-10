from pprint import pprint
from lxml import html
import requests
import datetime
from pymongo import MongoClient

def get_yandex(link):
    response = requests.get(link, headers=header)
    dom = html.fromstring(response.text)
    items = dom.xpath("//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']/div[@class='mg-grid__col mg-grid__col_xs_4'] | //div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']/div[@class='mg-grid__col mg-grid__col_xs_8']")
    #print(items)
    news = []
    for item in items:
        news1 = {}
        news1['header'] = item.xpath(".//h2/text()")[0]
        news1['link'] = item.xpath(".//a[@class='news-card__link']/@href")[0]
        news1['source'] = item.xpath(".//span[@class='mg-card-source__source']//text()")[0]
        news1['date'] = datetime.date.today().strftime("%d.%m.%Y")
        #print(news1['header'], news1['link'], news1['source'], news1['date'])
        news.append(news1)
    return news

# Yandex News
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
main_link = 'https://yandex.ru/news/'
news_array = get_yandex(main_link)

#Mail.ru
main_link = 'https://news.mail.ru/'

response = requests.get(main_link,headers=header)
dom = html.fromstring(response.text)


items = dom.xpath('//div[@class="cols__inner"]//a[@href="/politics/"]/../../..//li | .//div[@class="cols__inner"]//a[@href="/politics/"]//../../..//a[@class="newsitem__title link-holder"]/@href')


links = [items[0]]
news = []
for item in items[1:]:
    link = item.xpath(".//a[@class='link link_flex']/@href")
    links.append(link[0])
#print(links)

for link in links:
    news1 = {}
    news1['link'] = link
    response = requests.get(link, headers=header)
    dom = html.fromstring(response.text)
    news1['header'] = dom.xpath('//h1[@class="hdr__inner"]//text()')[0]
    news1['date'] = dom.xpath('//span[@datetime]/@datetime')[0][:10]
    news1['source'] = dom.xpath('//a[@class="link color_gray breadcrumbs__link"]//text()')[0]
    news.append(news1)
news_array += news

#Lenta
main_link = "https://lenta.ru/"
response = requests.get(main_link,headers=header)
dom = html.fromstring(response.text)

items = dom.xpath('//time[@class="g-time"]/../../a')
#print(items)
for item in items:
    news1 = {}
    news1['date'] = item.xpath('.//time/@datetime')[0].strip()
    news1['header'] = item.xpath('.//time/../text()')[0].replace("\xa0", "")
    news1['source'] = 'Lenta.ru'
    news1['link'] = main_link + item.xpath('.//time/../@href')[0]
    #print(news1)
    news_array.append(news1)


pprint(news_array)

client = MongoClient('127.0.0.1',27017)
db = client['users_db']

news_db = db.news
news_db.insert_many(news_array)
