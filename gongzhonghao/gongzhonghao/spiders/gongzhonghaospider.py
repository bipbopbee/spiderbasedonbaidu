# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from gongzhonghao.items import GongzhonghaoItem
import re
#解决utf8 code问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class GongzhonghaospiderSpider(RedisSpider):
    name = 'gongzhonghaospider'
    
    redis_key = "gongzhonghao:start_urls"

    def parse(self, response):
        data = response.body
        pattern1 = re.compile(r'var nickname = \S*\;')
        pattern2 = re.compile(r'var msg_title = \S*\;')
        pattern3 = re.compile(r'(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)')

        item = GongzhonghaoItem()
        item['url'] = response.url
        item['publishname']  = pattern1.findall(data)[0]
        pattern4 = re.compile('\"(.*?)\"')
        item['publishname']  = pattern4.findall(item['publishname'])[0]
        item['title']  = pattern2.findall(data)[0]
        item['title']  = pattern4.findall(item['title'])[0]
        item['publishdate']  =  pattern3.findall(data)[0][0]

        self.logger.debug("url" + item['url'][0])
        self.logger.debug("publishname" + item['publishname'][0])
        self.logger.debug("title" + item['title'][0])
        self.logger.debug("publishdate" + item['publishdate'])
        yield item

