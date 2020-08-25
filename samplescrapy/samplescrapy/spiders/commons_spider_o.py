# -*- coding: utf-8 -*-
import math

import scrapy
from samplescrapy.product2 import ItemCompleted
from scrapy.loader import ItemLoader
from selenium import webdriver
import geckodriver_autoinstaller
from scrapy.shell import inspect_response


class CommonstestSpider(scrapy.Spider):
    name = 'Commons'
    #start_urls = ['https://www.oercommons.org/browse?batch_size=20&sort_by=title&view_mode=summary&f.language=en']
    query_url = "https://www.oercommons.org/browse?batch_size=100&batch_start={}&f.language=es"

    def start_requests(self):
        start_url = self.query_url.format(0)
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        # inspect_response(response, self)
        yield self.parse_page(response)
        items_number = int(response.css('.items-number ::text').extract_first())
        for index in list(range(1, math.ceil(items_number / 100))):
            next_url = self.query_url.format(index * 100)
            yield scrapy.Request(url=next_url, callback=self.parse_page)

    def parse_page(self, response):
        # inspect_response(response, self)
        for commons in response.xpath(
                '//article[@class="js-index-item index-item clearfix"]'):
            item_url = commons.xpath('.//div[@class="item-title"]/a/@href').extract_first()
            yield scrapy.Request(
                url=item_url,
                callback=self.parse_item,
            )

    # def parse(self, response):
    #    inspect_response(response, self)
    #    for commons in response.xpath('//article[@class="js-index-item index-item clearfix"]'):
    #        loader = ItemLoader(item=ItemCompleted(), selector=commons)
    #        loader.add_xpath('link', './/div[@class="item-title"]/a/@href')
    #        item = loader.load_item()
    #        return scrapy.Request(url=item['link'][0], callback=self.parse_mongo,
    #                              meta={'item': item})
    #    next_page = response.xpath('//div[@class="pagination"]/a/@href').extract_first()
    #    if next_page is not None:
    #        next_page_link = response.urljoin(next_page)
    #        yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_item(self, response):
        # inspect_response(response, self)
        loader = ItemLoader(item=ItemCompleted(), selector=response)

        loader.add_value('link', response.url)
        loader.add_xpath('title',
                         'normalize-space(.//h1[@class="material-title"]/a/text())')
        loader.add_xpath('overview',
                         'normalize-space(.//dl[@class="materials-details-abstract"]/dd/text())')
        loader.add_xpath('subject',
                         'normalize-space(.//dl[@class="materials-details-first-part"]/dd'
                         '/span[@itemprop="about"]/text())')
        loader.add_xpath('material_type',
                         'normalize-space(.//dl[@class="materials-details-first-part"]/dd/'
                         'span[@itemprop="learningResourceType"]/text())')
        loader.add_xpath('author', './/dl[@class="materials-details-first-part"]'
                                   '/dd/span[@itemprop="author"]/text()')
        loader.add_xpath('level',
                         'normalize-space(.//dl[@class="materials-details-first-part"]/dd[2]/text())')
        yield loader.load_item()

    def parse_mongo(self, response):
        inspect_response(response, self)
        for commons in response.xpath('//article[@class="item view-item"]'):
            item = response.meta['item']
            itemnew = ItemLoader(item, selector=commons)
#            url = response.url
#            print('****************************')
#            print(url)
#            itemnew.replace_value('link', url, input_processor=MapCompose(remove_tags), output_processor=Identity())
            itemnew.add_xpath('title', 'normalize-space(.//h1[@class="material-title"]/a/text())')
            itemnew.add_xpath('overview', 'normalize-space(.//dl[@class="materials-details-abstract"]/dd/text())')
            itemnew.add_xpath('subject', 'normalize-space(.//dl[@class="materials-details-first-part"]/dd'
                                         '/span[@itemprop="about"]/text())')
            itemnew.add_xpath('material_type', 'normalize-space(.//dl[@class="materials-details-first-part"]/dd/'
                                               'span[@itemprop="learningResourceType"]/text())')
            itemnew.add_xpath('author', './/dl[@class="materials-details-first-part"]'
                                        '/dd/span[@itemprop="author"]/text()')
            itemnew.add_xpath('level', 'normalize-space(.//dl[@class="materials-details-first-part"]/dd[2]/text())')
#            print("****************************")
            yield itemnew.load_item()