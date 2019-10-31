# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from zhihuuser.items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user = 'excited-vczh'
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    follow_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit=20'
    follow_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)
        yield Request(self.follow_url.format(user=self.start_user, include=self.follow_query, offset=0), callback=self.parse_follow)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        item['id'] = result['id']
        item['name'] = result['name']
        item['avatar_url'] = result['avatar_url']  # 头像
        item['follower_count'] = result['follower_count']  # 粉丝数
        item['headline'] = result['headline']  # 签名
        item['user_url'] = result['url']  # 主页
        item['gender'] = result['gender']
        item['url_token'] = result['url_token']
        yield item

        yield Request(self.follow_url.format(user=result.get('url_token'), include=self.follow_query, offset=0),callback=self.parse_follow)


    def parse_follow(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys() and results['data']:
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)
        if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
            next_page = result.get('paging').get('next')
            yield Request(next_page, callback=self.parse_follow)


