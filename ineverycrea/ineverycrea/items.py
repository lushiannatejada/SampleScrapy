import scrapy
from scrapy.item import Field
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


class ItemInevery(scrapy.Item):
    title = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    link = Field(input_processor=MapCompose(remove_tags))
    overview = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    subject = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    author = Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())