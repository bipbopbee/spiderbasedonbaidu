#coding=utf-8
import urllib
import urllib2
import re
import time
from SpiderLogger import logger
from csimulate import getLineFileFunc
#解决utf8 code问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import socket
socket.setdefaulttimeout(10.0)
from opredis import lpush

def getsearchpagebykeyword(url, keyword):
    strWd = {'wd':keyword}
    strWd = urllib.urlencode(strWd)
    strFullurl = url + strWd
    return geturlpage(strFullurl)

def geturlpage(url):
    strData = ''
    strHeaders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    objRequest = urllib2.Request(url = url, headers = strHeaders)
    try:
        objResponse = urllib2.urlopen(objRequest, data = None, timeout = 10)
        strData = objResponse.read()
    except urllib2.HTTPError, err:
        print url + bytes(err.code)
    except urllib2.URLError, err:
        print err
        print url
    except Exception, e:
        print 'timeout'
    return strData

#@return 返回视频网址list和下一页网址
def resolvepagedata(data):
    arrList = []
    strRetnexturl = ''
    objSoup = BeautifulSoup(data, 'lxml')
    tmpnexturl = objSoup.find(name='a', text='下一页>')
    if tmpnexturl:
        strRetnexturl = tmpnexturl.get('href')
    for link in objSoup.find_all(name='a', attrs={'href':re.compile(r'^http:')}):
        arrList.append(link.get('href'))
    return (arrList, strRetnexturl)

#@return 返回码流地址
#测试地址1.https://www.haokongbu.com/play/471931.html
def getvideoadress(url):
    strData = geturlpage(url)
    strUrlfilter = r'(?:https|http)://.+?\.(?:mp4|m3u8|mkv)'
    pattern = re.compile(strUrlfilter)
    return pattern.findall(strData)

def main(argv):
    argc = len(argv)
    keyword = ''
    if argc == 1:
        print 'Useage:python searchengine.py {keyword1} {keyword2} ...'
        return
    for i in range(argc):
        if i == 0:
            continue
        keyword = keyword + argv[i] + ' '
    url = "http://www.baidu.com/s?"
    searchcount = 50
    n = 0
    data = getsearchpagebykeyword(url, keyword)
    while n < searchcount:
        websiteslist, nexturl = resolvepagedata(data)
        for website in websiteslist:
            #print getvideoadress(website)
            lpush('myspider:start_urls', website)
        data = geturlpage(url[:-3] + nexturl)
        n = n + 1
if __name__ == '__main__':
    #lpush('myspider:start_urls', 'https://list.youku.com/category/show/c_85.html')
    #main(sys.argv)
        #   href="/category/show/c_96.html">电影</a><a class=""
        #                                 href="/category/show/c_85.html">综艺</a><a class=""
        #                                 href="/category/show/c_100.html">动漫</a><a class=""
        #                                 href="/category/show/c_177.html">少儿</a><a class=""
        #                                 href="/category/show/c_95.html">音乐</a><a class=""
        #                                 href="/category/show/c_87.html">教育</a><a class=""
        #                                 href="/category/show/c_84.html">纪录片</a><a class=""
        #                                 href="/category/show/c_98.html">体育</a><a class=""
        #                                 href="/category/show/c_178.html">文化</a><a class=""
        #                                 href="/category/show/c_86.html">娱乐</a><a class=""
        #                                 href="/category/show/c_99.html">游戏</a><a class=""
        #                                 href="/category/video/c_91.html">资讯</a><a class=""
        #                                 href="/category/video/c_94.html">搞笑</a><a class=""
        #                                 href="/category/video/c_103.html">生活</a><a class=""
        #                                 href="/category/video/c_104.html">汽车</a><a class=""
        #                                 href="/category/video/c_105.html">科技</a><a class=""
        #                                 href="/category/video/c_89.html">时尚</a><a class=""
        #                                 href="/category/video/c_90.html">亲子</a><a class=""
        #                                 href="/category/video/c_88.html">旅游</a><a class=""
        #                                 href="/category/video/c_171.html">微电影</a><a class=""
        #                                 href="/category/video/c_172.html">网剧</a><a class=""
        #                                 href="/category/video/c_174.html">拍客</a><a class=""
        #                                 href="/category/video/c_175.html">创意视频</a></dd>
    print geturlpage('https://list.youku.com/category/show/c_85.html')


    
    