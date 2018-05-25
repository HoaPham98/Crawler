# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviesItem(scrapy.Item):
    url = scrapy.Field()
    _id = scrapy.Field()
    poster_vertical = scrapy.Field()
    pass

class DetailsItem(scrapy.Item):
    data = scrapy.Field()

    pass
