import scrapy
from scrapy.http import HtmlResponse
from lermer.items import LermerItem
from scrapy.loader import ItemLoader

class CastoSpider(scrapy.Spider):
    name = 'casto'
    allowed_domains = ['castorama.ru']


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("search")}/']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='product-card__img-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LermerItem(), response=response)
        loader.add_xpath('name', "//div[contains(@class,'product-essential__left-col')]/h1/text()")
        loader.add_xpath('price', "//span[@class='price']//text()")
        loader.add_xpath('curr', '//span[@class="price"]//span[@class="currency"]//text()')
        loader.add_xpath('photos', "//div/descendant-or-self::img[@class='thumb-slide__img swiper-lazy swiper-lazy-loaded']/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()