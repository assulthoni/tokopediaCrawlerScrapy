import json
import scrapy
from ..items import TokopediacrawlerItem
from scrapy.linkextractors import LinkExtractor

from scrapy_splash import SplashRequest

class TokopediaSpiderSpider(scrapy.Spider):
    name = 'tokopedia_spider'
    start_urls = ['https://www.tokopedia.com/p/buku/komputer-internet/buku-programming']

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    def parse(self, response):
        # print(response.text)
        items = TokopediacrawlerItem()
        DOM = response.css('script').extract()
        print(DOM)
        for d in DOM:
            yield d
