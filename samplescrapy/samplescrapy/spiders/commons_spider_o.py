# -*- coding: utf-8 -*-
import scrapy
from samplescrapy.product2 import ItemCompleted
from scrapy.loader import ItemLoader
from selenium import webdriver
import geckodriver_autoinstaller
from scrapy.shell import inspect_response


class CommonstestSpider(scrapy.Spider):
    name = 'Commons'
    start_urls = ['https://www.oercommons.org/browse?batch_size=20&sort_by=title&view_mode=summary&f.language=en']

    def __init__(self):
        geckodriver_autoinstaller.install()
        self.driver = webdriver.Firefox()

    def parse(self, response):
        inspect_response(response, self)
        for commons in response.xpath('//article[@class="js-index-item index-item clearfix"]'):
            loader = ItemLoader(item=ItemCompleted(), selector=commons)
            loader.add_xpath('link', './/div[@class="item-title"]/a/@href')
            item = loader.load_item()
            return scrapy.Request(url=item['link'][0], callback=self.parse_mongo,
                                  meta={'item': item})
        next_page = response.xpath('//div[@class="pagination"]/a/@href').extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)


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