import scrapy


class TableSpider(scrapy.Spider):
    name = 'table'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['http://en.wikipedia.org/wiki/List_of_United_States_cities_by_population']

    def parse(self, response):
        table = response.xpath('//*[@id="mw-content-text"]/div[1]/table[5]')
        # table = response.xpath('//table[contains(@class, "wikitabe sortable"]')[0]

        trs = table.xpath('.//tr')[1:]
        for tr in trs:
            rank = tr.xpath('.//td[1]/text()').extract_first().strip()
            city = tr.xpath('.//td[2]//text()').extract_first()
            state = tr.xpath('.//td[3]/text()|.//td[3]/a/text()').extract_first().strip()

            yield {
            "rank":rank,
            "city":city,
            "state":state
            }

"""
//*[@id="mw-content-text"]/div[1]/table[5]/tbody/tr[1]/td[3]/a
"""