# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy

from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["erowid.org"]
    start_urls = [
        "https://www.erowid.org/experiences/exp_list.shtml"
    ]

    # def parse_items(self, response):
    #     item = DmozItem()
    #     items = []
    #     item['desc'] = response.xpath('//div[@class="report-text-surround"]/text()').extract()
    #     item['name'] = response.xpath('//div[@class="substance"]/text()').extract()
    #     items.append(item)
    #
    #     yield item
    #     return(items)

    def parse(self, response):
        for item in response.xpath('//ul[@type="CIRCLE"]/li/a/@href').extract():
            yield scrapy.Request(url="https://www.erowid.org/experiences/" + item, callback=self.page_1, errback=self.errback_httpbin)

    def page_1(self, response):
        for item in response.xpath('//td/a/@href').extract():
            yield scrapy.Request(url="https://www.erowid.org" + item, callback=self.page_2)

    def page_2(self, response):
        item = DmozItem()
        items = []
        item['name'] = response.xpath('//div[@class="substance"]/text()').extract()
        item['desc'] = response.xpath('//div[@class="report-text-surround"]/text()').extract()
        items.append(item)
        return(items)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))
