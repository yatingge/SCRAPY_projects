# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor


# class BooksSpider(CrawlSpider):
#     name = 'books'
#     allowed_domains = ['books.toscrape.com']
#     start_urls = ['https://books.toscrape.com/', ]

#     rules = (Rule(LinkExtractor(), callback='parse_page', follow=True), )

#     def parse_page(self, response):
#         # yield {'URL', response.url}
#         pass

# from scrapy import Spider
# from scrapy.selector import Selector
# from scrapy.http import Request
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from time import sleep

# class BooksSpider(Spider):
#     name = 'books'
#     allowed_domains = ['books.toscrape.com']

#     def start_requests(self):
#         # create a web driver instance
#         self.driver = webdriver.Chrome('/Users/yatingge/Downloads/chromedriver')
#         # navigate to a web page
#         self.driver.get('http://books.toscrape.com')

#         # locate a web page element
#         # preload user actions
#         sel = Selector(text=self.driver.page_source)
#         books = sel.xpath('//h3/a/@href').extract()
#         for book in books:
#             url = 'https://books.toscrape.com/' + book
#             yield Request(url, callback=self.parse_book)

#         # locate a web page element
#         # preload user actions
#         while True:
#             try:
#                 next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
#                 sleep(3)
#                 self.logger.info('Sleeping for 3 seconds.')
#                 next_page.click()

#                 sel = Selector(text=self.driver.page_source)
#                 books = sel.xpath('//h3/a/@href').extract()
#                 for book in books:
#                     url = 'https://books.toscrape.com/catalogue/' + book
#                     yield Request(url, callback=self.parse_book)

#             except NoSuchElementException:
#                 self.logger.info('No more pages to load.')
#                 self.driver.quit()
#                 break

#     def parse_book(self, response):
#         title = response.css('h1::text').extract_first()
#         url = response.request.url
#         yield {'title':title, 'url':url}

import os
import glob
from scrapy import Spider
from scrapy.http import Request

def product_description(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    # start_urls = ['https://books.toscrape.com']

    def __init__(self, category):
        # scrapy crawl books -a category='https://books.toscrape.com/catalogue/category/books/thriller_37/index.html'
        self.start_urls = [category]

    def parse(self, response):
        books = response.xpath('//h3//a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # process next page
        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)


    def parse_book(self, response):
        title = response.xpath('//h1/text()').extract()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()

        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace("../../", 'https://books.toscrape.com/')

        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')

        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        # get product information from table
        upc = product_description(response, 'UPC')
        tax = product_description(response, 'Tax')

        yield {
            'title' : title,
            'price' : price,
            'image_url' : image_url,
            'rating': rating,
            'description' : description,
            'upc' : upc,
            'tax' : tax
        }

    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        os.rename(csv_file, 'foobar.csv')







