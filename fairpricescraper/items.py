# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class FairpricescraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand_name = scrapy.Field()
    product_name = scrapy.Field()
    original_price = scrapy.Field()
    offer_price = scrapy.Field()
    offer_description = scrapy.Field()
    stock = scrapy.Field()
    dietary_attributes = scrapy.Field()
    halal = scrapy.Field()
    image_url = scrapy.Field()
    weight = scrapy.Field()
    country_of_origin = scrapy.Field()
    rating = scrapy.Field()
    category = scrapy.Field()
