from lxml import html
import requests
import unicodedata
import datetime
from pymongo import MongoClient

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

url = 'https://yandex.ru/news/'

session = requests.Session()
response = session.get(url, headers=header)

dom = html.fromstring(response.text)

news_sources = dom.xpath("//a[contains(@class,'mg-card__source-link')]/@aria-label")
news_sources = [i.replace('Источник: ','') for i in news_sources]

news_names = dom.xpath("//h2[@class='mg-card__title']//text()")
news_names = [unicodedata.normalize("NFKD", i) for i in news_names]

news_links = dom.xpath("//h2[contains(@class,'mg-card__title')]//@href")

x = datetime.datetime.now()
news_times = dom.xpath("//span[@class='mg-card-source__time']/text()")
news_times = [f"{x.day}-{x.month}-{x.year}" if i.find('вчера в ') else f"{x.day - 1}-{x.month}-{x.year}" for i in news_times]

client = MongoClient('127.0.0.1', 27017)

mongo_db = client["news_db"]
mongo_col = mongo_db["yandex_news"]

for i in range(len(news_names)):
    y = mongo_col.update_one({"Источник": news_sources[i],
                                  "Новость": news_names[i],
                                  "Ссылка": news_links[i],
                                  "Дата": news_times[i]},
                             { "$set":{"Источник": news_sources[i],
                                  "Новость": news_names[i],
                                  "Ссылка": news_links[i],
                                  "Дата": news_times[i]}}, upsert=True)

count = 0

for x in mongo_col.find():
    count += 1

print(f'\nОбщее число записей в базе: {count}')