# -*- coding: utf-8 -*-
import scrapy
from samplescrapy.items import DemoItem
from scrapy.loader import ItemLoader
from scrapy.shell import inspect_response
from scrapy.http import FormRequest
from selenium import webdriver
import geckodriver_autoinstaller


class ProComun(scrapy.Spider):
    name = 'ProComun'
    current_page = 0
    #start_urls = ['http://procomun.educalab.es/search/search.php']
    url = "http://procomun.educalab.es/search/search.php"

    def start_requests(self):
        frmdata = {"query": "", "page": '0', "type": "LEARNING_RESOURCES", "uid": '0', "language[language]": "es",
                   "sort": "publicationDate-DESC"}
        yield FormRequest(self.url, formdata=frmdata, callback=self.parse)

    def parse(self, response):
        print(response)
        enlaces = response.xpath('//h2[@class="title"]/a/@href').extract()
        #enlaces = response.css('h2.title ::attr(href)').extract()
        print(enlaces)
        for link in enlaces:
            print("++++++++++++++++++")
            loader = ItemLoader(item=DemoItem(), selector=link)
            loader.add_xpath('link', link)
            item = loader.load_item()
            www = 'http://procomun.educalab.es/'
            url = item['link'][0]
            return scrapy.Request(www + url, callback=self.parse_mongo, meta={'item': item})
        # cambiar paginacion
        self.current_page = self.current_page + 1
        frmdata = {"query": "", "page": str(self.current_page), "type": "LEARNING_RESOURCES", "uid": '0',
                       "language[language]": "es", "sort": "publicationDate-DESC"}
        yield FormRequest(url=self.url, formdata=frmdata, callback=self.parse)

    def parse_mongo(self, response):
        inspect_response(response, self)
        for commons in response.xpath('//article[@class="clearfix center"]'):
            item = response.meta['item']
            itemnew = ItemLoader(item, selector=commons)
            itemnew.add_xpath('title', 'normalize-space(.//div[@class="detail-title"]/h1/text())')
            itemnew.add_xpath('overview', 'normalize-space(.//div[@class="detail-ode-description"]/p/text())')
            itemnew.add_xpath('subject', 'normalize-space(.//div[@class="detail-ode-knowledge-area clearfix"]/a/text())')
            itemnew.add_xpath('material_type', 'normalize-space(.//div[@class="detail-ode-resource-type clearfix"]/a/text())')
            itemnew.add_xpath('author', 'normalize-space(.//div[@class="detail-ode-authors"]/div/span/a/text())')
            itemnew.add_xpath('level', 'normalize-space(.//div[@class="detail-ode-learning-context clearfix"]/a/text())')
            yield itemnew.load_item()
