import json
import scrapy
from ..items import TokopediacrawlerItem
from selenium import webdriver

class TokopediaSpiderSpider(scrapy.Spider):
    name = 'tokopedia_spider'
    start_urls = ['https://www.tokopedia.com/p/buku/komputer-internet/buku-programming']

    def parse(self, response):
        # print(response.text)
        items = TokopediacrawlerItem()
        # DOM = response.css('script').extract()
        # print(DOM)
        # for d in DOM:
        #     yield d
        pass
