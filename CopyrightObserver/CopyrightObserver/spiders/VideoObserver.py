# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from CopyrightObserver.items import CopyrightobserverItem
import re
#解决utf8 code问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class VideoobserverSpider(RedisSpider):
    name = 'VideoObserver'
    #allowed_domains = ['www.baidu.com']
    #start_urls = ['http://www.baidu.com/']
    redis_key = "myspider:start_urls"

    #__instance__ = None

    # def __new__():
    #     if not cls.__instance__:
    #         cls.__instance__ = object.__new__(cls)
    #     else:
    #         return cls.__instance__

    def __init__(self, apitoken):
        self.apitoken = apitoken
        return super(VideoobserverSpider, self).__init__()

    def parse(self, response):
        data = response.body
        strUrlfilter = r'(?:https|http)://.+?\.(?:mp4|m3u8|mkv|MP4|M3U8|MKV)'
        pattern = re.compile(strUrlfilter)
        if len(pattern.findall(data)) > 0:
            if len(pattern.findall(data)[0]) > 100:
                return
            item = CopyrightobserverItem()
            item['detailurl'] = response.url
            item['videourl']  = pattern.findall(data)[0]
            item['apitoken']  = self.apitoken
            yield item
        else:
            nexturls = response.xpath('//a/@href').extract()
            for nexturl in nexturls:
                yield scrapy.Request(url = nexturl, callback = self.parse_nextpage, dont_filter=True)
    
    def parse_nextpage(self, response):
        data = response.body
        strUrlfilter = r'(?:https|http)://.+?\.(?:mp4|m3u8|mkv)'
        pattern = re.compile(strUrlfilter)
        if len(pattern.findall(data)) > 0:
            if len(pattern.findall(data)[0]) > 100:
                return
            item = CopyrightobserverItem()
            item['detailurl'] = response.url
            item['videourl']  = pattern.findall(data)
            item['apitoken']  = self.apitoken
            yield item
