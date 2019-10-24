# -*- coding: utf-8 -*-
import scrapy
from samplescrapy.product2 import ItemCompleted
from pymongo import MongoClient
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Identity, MapCompose
from w3lib.html import remove_tags


class CommonstestSpider(scrapy.Spider):
    name = 'commonstest'

#    allowed_domains = ['oercommons.org']
    start_urls = ['https://www.oercommons.org/browse?batch_size=100&sort_by=title&view_mode=list&f.language=es']

    def parse(self, response):
        for commons in response.xpath('//article[@class="js-index-item index-item clearfix"]'):
            loader = ItemLoader(item=ItemCompleted(), selector=commons)
            loader.add_xpath('link', './/div[@class="item-title"]/a/@href')
            item = loader.load_item()
            yield scrapy.Request(url=item['link'][0], callback=self.parse_mongo, meta={'item': item})

        next_page = response.xpath('//div[@class="pagination"]/a/@href').extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_mongo(self, response):
        for commons in response.xpath('//article[@class="item view-item"]'):
            item = response.meta['item']
            itemnew = ItemLoader(item, selector=commons)
            url = response.url
            print('****************************')
            print(url)
            itemnew.replace_value('link', url, input_processor=MapCompose(remove_tags), output_processor=Identity())
            itemnew.add_xpath('title', './/h1[@class="material-title"]/a/text()')
            itemnew.add_xpath('overview', './/dl[@class="materials-details-abstract"]/dd/text()')
            itemnew.add_xpath('subject', './/dl[@class="materials-details-first-part"]/dd/span[@itemprop="about"]'
                                         '/text()')
            itemnew.add_xpath('material_type', './/dl[@class="materials-details-first-part"]/dd/'
                                               'span[@itemprop="learningResourceType"]/text()')
            itemnew.add_xpath('author', './/dl[@class="materials-details-first-part"]/dd/span[@itemprop="author"]'
                                        '/a/text()')
#            print("****************************")
            yield itemnew.load_item()