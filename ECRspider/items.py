# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class EcrspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GoodsItem(scrapy.Item):
    GOODS_ID = scrapy.Field()
    GOODS_NAME = scrapy.Field()
    GOODS_URL = scrapy.Field()
    # GOODS_PRICE = scrapy.Field()
    # MONTHLY_SALES = scrapy.Field()
    TOTAL_COMMENT = scrapy.Field()


class CommentsItem(scrapy.Item):
    GOODS_ID = scrapy.Field()
    COMMENTS = scrapy.Field()
