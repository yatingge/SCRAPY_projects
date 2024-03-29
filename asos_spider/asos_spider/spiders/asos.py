import json
from scrapy import Spider
from scrapy.http import Request


class AsosSpider(Spider):
    name = 'asos'
    allowed_domains = ['asos.com']
    start_urls = ['https://www.asos.com/men/shoes-boots-trainers/boots/cat/?cid=5774&nlid=mw%7Cshoes%7Cshop%20by%20product%7Cboots&page=1']

    def parse(self, response):
        products = response.xpath('//article[@data-auto-id="productTile"]/a/@href').extract()
        for product in products:
            yield Request(product,callback=self.parse_shoe)

        next_page_url = response.xpath('//a[text()="Load more"]/@href').extract_first()
        if next_page_url:
            yield Request(next_page_url,
                callback=self.parse)


    def parse_shoe(self, response):
        product_name = response.xpath('//h1/text()').extract_first()
        product_id = response.url.split('/prd/')[1].split('?')[0]
        price_api_url = 'https://www.asos.com/api/product/catalogue/v3/stockprice?productIds=' + product_id + '&store=COM&currency=GBP'

        yield Request(
            price_api_url,
            meta={'product_name': product_name},
            callback=self.parse_shoe_price)


    def parse_shoe_price(self, response):
        jsonresponse = json.loads(response.body.decode('utf-8'))
        price = jsonresponse[0]['productPrice']['current']['text']

        yield {'product_name': response.meta['product_name'],
        'price': price}


