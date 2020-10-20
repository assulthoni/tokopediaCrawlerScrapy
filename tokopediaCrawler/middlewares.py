# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

# selenium
from selenium import webdriver

class TokopediacrawlerSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TokopediacrawlerDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RotateAgentMiddleware(object):

    def process_request(self, request, spider):
         # webdriver setting
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        # webdriver request
        driver = webdriver.Chrome(chrome_options=options,
                                    executable_path="D:/kuliah/TUGAS AKHIR/SCRAPING TOKOPEDIA/chromedriver.exe"
                                    )
        driver.get("https://deviceatlas.com/blog/list-of-user-agent-strings")
        time.sleep(1)

        # real time random select user agent from website
        agent_list = driver.find_elements_by_xpath("//td")
        agent = (random.choice(agent_list)).text
        loguru.logger.info("Hold Agent {agent}".format(agent=agent))
        driver.quit()

        # hold user agent
        request.headers["User-Agent"] = agent

class SeleniumMiddleware(object):

    def process_request(self, request, spider):

        # webdriver setting
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server=%s' % request.meta["proxy"])
        options.add_argument('--user-agent=%s' % request.headers["User-Agent"])

        # webdriver request
        driver = webdriver.Chrome(chrome_options=options,
                                  executable_path="D:/kuliah/TUGAS AKHIR/SCRAPING TOKOPEDIA/chromedriver.exe"
        )
        driver.get(request.url)
        time.sleep(10)

        return scrapy.http.HtmlResponse(url=request.url,
                                        status=200,
                                        body=driver.page_source
                                                   .encode("utf-8"),
                                        encoding="utf-8")


class TokopediaMiddleware(object):
    def process_request(self, request, spider):
        url = request.url
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('--proxy-server=%s' % request.meta["proxy"])
        # options.add_argument('--user-agent=%s' % request.headers["User-Agent"])

        # webdriver request
        driver = webdriver.Chrome(chrome_options=options,
                                 executable_path="D:/kuliah/TUGAS AKHIR/SCRAPING TOKOPEDIA/chromedriver.exe"
        )
        driver.set_window_size(1440, 800)
        driver.delete_all_cookies()
        driver.get(url)

        carousel_xpath = (
            "//*[@id="zeus-root"]/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[4]/div[1]",
            
        )
        books = driver.find_elements_by_xpath(carousel_xpath)
        for book in books:
            print(book)

