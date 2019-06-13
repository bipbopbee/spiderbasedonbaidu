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
#for link in objSoup.find_all(name='a', attrs={'href':re.compile(r'^http:')}):
#        arrList.append(link.get('href'))
    def parse(self, response):
        node_list = response.xpath('//div[@class="pack_info_list"]')
        for node in node_list:
            title = node.xpath('.//a/text()').extract_first()
            subtitle = node.xpath('//div[@class="pack_subtitle"]/text()').extract_first()
            detail_url = node.xpath('.//a/@href').extract_first()
            self.logger.debug("标题:" + title)
            self.logger.debug('子标题：' + subtitle)
            self.logger.debug('详情页：http:' + detail_url)
            yield scrapy.Request(url = 'http:' + detail_url, meta = {'title':title,'subtitle':subtitle},
                                callback=self.parse_detail, dont_filter=True)

        # request_url=

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