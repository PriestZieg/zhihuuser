# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    avatar_url = scrapy.Field()
    follower_count = scrapy.Field()
    headline = scrapy.Field()
    user_url = scrapy.Field()
    gender = scrapy.Field()
    url_token = scrapy.Field()
