from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instaparser.spiders.instaspider import InstaspiderSpider
from instaparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaspiderSpider)

    process.start()
