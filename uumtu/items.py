# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MoteItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mote = Field()
    url = Field()
    title = Field()

class XingganItem(Item):
    url = Field()
    title = Field()
    website = Field()