from scrapy import Spider
from scrapy.http import Request, FormRequest

class EplanningSpider(Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response):
        urls = response.xpath('//a/@href').extract()
        for url in urls[:10]:
            if url == '#':
                pass
            else:
                yield Request(
                    url=url,
                    callback=self.parse_application)

    def parse_application(self, response):
        # app_url = response.xpath('/html/body/div[2]/div/div/div[2]/div[1]/a/@href').extract_first()
        app_url = response.xpath('//*[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').extract_first()
        yield Request(response.urljoin(app_url),
            callback=self.parse_form)

    def parse_form(self, response):
        yield FormRequest.from_response(
            response,
            formdata={'RdoTimeLimit': '42'},
            dont_filter=True,
            # formxpath='/html/body/div[2]/form',
            formxpath='(//form)[2]',
            callback=self.parse_pages)

    def parse_pages(self, response):
        application_urls = response.xpath('//td/a/@href').extract()
        for url in application_urls:
            url = response.urljoin(url)
            yield Request(
                url,
                callback=self.parse_items)

        next_page_url = response.xpath('//*[@rel="next"]/@href').extract_first()
        if next_page_url:
            absolute_next_page_url = response.urljoin(next_page_url)
            yield Request(
                absolute_next_page_url,
                callback=self.parse_items)

    def parse_items(self, response):
        agent_btn = response.xpath('//*[@value="Agents"]/@style').extract_first()

        if agent_btn and 'display: inline;  visibility: visible;' in agent_btn:

            name = response.xpath('//tr[th="Name :"]/td/text()').extract_first()

            address_first = response.xpath('//tr[th="Address :"]/td/text()').extract()
            address_second =  response.xpath('//tr[th="Address :"]/following-sibling::tr/td/text()').extract()[:3]
            address = address_first + address_second

            phone = response.xpath('//tr[th="Phone :"]/td/text()').extract_first()
            fax = response.xpath('//tr[th="Fax :"]/td/text()').extract_first()
            email = response.xpath('//tr[th="e-mail :"]/td/a/text()').extract_first()

            url = response.url

            yield {"name":name,
                "address":address,
                "phone":phone,
                "fax":fax,
                "email":email,
                "url":url}

        else:
            self.logger.info('Agent botton not found on page, passing invalid url')








