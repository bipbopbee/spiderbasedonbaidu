#coding=utf-8
import urllib
import urllib2
import re
import time
import random
#from SpiderLogger import logger
#from csimulate import getLineFileFunc
#解决utf8 code问题
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
import socket
socket.setdefaulttimeout(10.0)
from opredis import lpush
proxy_list = [
    {"http" : "120.83.110.203:9999"},
    {"http" : "120.83.107.126:9999"},
    {"http" : "182.35.87.208:9999"},
    {"http" : "113.121.21.28:9999"},
    {"http" : "120.83.103.45:9999"}]



def getsearchpagebykeyword(url, keyword):
    strWd = {'query':keyword}
    strWd = urllib.urlencode(strWd)
    strFullurl = url + strWd + "&ie=gbk&_sug_=n&_sug_type_=&type=2&s_from=input"
    return geturlpage(strFullurl)

def geturlpage(url):
    #print url
    proxy = random.choice(proxy_list)
    httpproxy_handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(httpproxy_handler)

    strData = ''
    strHeaders = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    objRequest = urllib2.Request(url = url, headers = strHeaders)
    try:
        #objResponse = urllib2.urlopen(objRequest, data = None, timeout = 5)
        objResponse = opener.open(objRequest, data = None, timeout = 10)
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
    data=data.encode('utf-8')
    f = open("gongzhonghao.html", 'w')
    f.write(data)
    f.close()
    objSoup = BeautifulSoup(data, 'lxml')
    tmpnexturl = objSoup.find(name='a', text='下一页')
    print tmpnexturl
    if tmpnexturl:
        strRetnexturl = tmpnexturl.get('href')
    for link in objSoup.find_all(name='a', attrs={'data-share':re.compile(r'^http:')}):
        arrList.append(link.get('data-share'))
    return (arrList, strRetnexturl)

#@return 返回码流地址
#测试地址1.https://www.haokongbu.com/play/471931.html
def getvideoadress(url):
    strData = geturlpage(url)
    strUrlfilter = r'(?:https|http)://.+?\.(?:mp4|m3u8|mkv)'
    pattern = re.compile(strUrlfilter)
    if len(pattern.findall(strData)) > 0:
        print url
    return pattern.findall(strData)

def start_search(keyword):
    url = "https://weixin.sogou.com/weixin?"
    #searchcount = 50
    #n = 0
    data = getsearchpagebykeyword(url, keyword)
    while True:
        websiteslist, nexturl = resolvepagedata(data)
        for website in websiteslist:
            #print getvideoadress(website)
            lpush('myspider:start_urls', website)
        data = geturlpage(url[:-3] + nexturl)
        if nexturl is None:
            break
    return
        #n = n + 1

#https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E6%83%8A%E5%A5%87%E9%98%9F%E9%95%BF&ie=utf8&_sug_=n&_sug_type_=
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
    url = "https://weixin.sogou.com/weixin?"
    #searchcount = 50
    #n = 0
    data = getsearchpagebykeyword(url, keyword)
    while True:
        websiteslist, nexturl = resolvepagedata(data)
        for website in websiteslist:
            print website
            #lpush('gongzhonghao:start_urls', website)
        if nexturl == "":
            break
        data = geturlpage(url[:-1] + nexturl)
        #print url[:-1] + nexturl
        
        #n = n + 1
if __name__ == '__main__':
    main(sys.argv)


    
    