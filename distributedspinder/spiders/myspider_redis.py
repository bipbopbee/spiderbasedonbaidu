#coding=utf-8
from scrapy_redis.spiders import RedisSpider
import scrapy
import re
#解决utf8 code问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'myspider_redis'
    redis_key = 'myspider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        node_list = response.xpath('//ul[@class="info-list"]')
        for node in node_list:
            title = node.xpath('./li[@class="title"]/a/text()').extract_first()
            xactors = node.xpath('./li[@class="actor"]/a')
            actors = []
            for actor in xactors:
               actors.append(actor.xpath('text()').extract_first())
               actors.append(' ')
            detail_url = node.xpath('./li[@class="title"]/a/@href').extract_first()
            self.logger.debug("标题:" + title)
            if len(actors) != 0:
                self.logger.debug('演员:' + ''.join(actors))
            self.logger.debug('详情页：http:' + detail_url)
            yield scrapy.Request(url = 'http:' + detail_url, meta = {'title':title,'actors':actors},
                                callback=self.parse_detail, dont_filter=True)
        next_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_url is None:
            pass
        else:
            self.logger.debug('下一页：' + next_url)
            yield scrapy.Request(url = 'http:' + next_url, callback=self.parse)

    def parse_detail(self, response):
        #item = VideoinfoItem()
        #item['title'] = response.meta['title']
        #item['subtitle'] = response.meta['subtitle']
        data = response.body
        pattern1 = re.compile(r'var str = \S*\;')
        tmpVidourl = pattern1.findall(data)
        #item['videourl'] = tmpVidourl.split(" ")[-1]
        pattern2 = re.compile(r'var production = \S*\;')
        tmpProductinfo = pattern2.findall(data)
        #item['productinfo'] = tmpProductinfo.split(" ")[-1]
        #yield item

        pass