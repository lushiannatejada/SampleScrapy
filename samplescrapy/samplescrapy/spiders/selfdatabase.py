# -*- coding: utf-8 -*-
import scrapy

from samplescrapy.product2 import ItemCompleted
from pymongo import MongoClient
from scrapy.loader import ItemLoader
from pprint import pprint


class CommonsSpider(scrapy.Spider):
    name = 'commonsdb'

    def __init__(self, *args, **kwargs):
        self.cliente = MongoClient('localhost', 27017)
        db = self.cliente ['temoadb'] # you can add db-url and port as parameter to MongoClient(), localhost by default
        print("**********************************************")
        print(db.commons)
        self.start_urls = db.commons.find({},{"link":1,"_id":0})
#        for x in self.start_urls:
#            link = x["link"][0]
#            print("**********************************************")
#            print(link)
        super(CommonsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        for u in self.start_urls:
            link = u["link"][0]
            if link is not None:
                print(response.url)
                item = ItemCompleted()
                yield scrapy.Request(response.url, callback=self.parse_mongo, meta={'item': item})

    def parse_mongo(self, response):
        for commons in response.xpath('//article[@class="item view-item"]'):
            item = ItemLoader(item=response.meta['item'], selector=commons)
#            item = response.meta['item']
            l = ItemLoader(item=ItemCompleted(), selector=commons)
            item.add_xpath('title', './/h1[@class="material-title"]/a/text()')
            item.add_xpath('overview', './/dl[@class="material-details-abstract"]/dd/text()')
            item.add_xpath('subject', './/dl[@class="materials-details-first-part"]/dd/span[@itemprop="about"]/text()')
            item.add_xpath('material_type', './/dl[@class="materials-details-first-part"]'
                                            '/dd/span[@itemprop="learningResourceType"]/text()')
            item.add_xpath('author', './//dl[@class="materials-details-first-part"]/dd/span[@itemprop="author"]'
                                     '/a/text()')
            print("****************************")
            pprint(item.item)
            return item
