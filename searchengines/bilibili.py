#coding=utf-8
import urllib
import urllib2
import re
import time
import random
import requests
import ssl
import datetime
import sys
import os
import json
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
import socket
socket.setdefaulttimeout(10.0)
from opredis import lpush

num = 0
sys.path.append("..")
from database.dbHelper import *
from database.searchenginedbHelper import *
from database.opredis import *
dbhelper = mySqlHelper()
dbOperator = searchenginedbHelper()
test_apitoken = ""
def insert(keyword, title, detailurl, videourl, upname, apitoken):
    sql = "insert ignore into bilibili (keyword, title, detailurl, videourl, upname, apitoken) values (%s, %s, %s, %s,%s,%s)"
    params = (keyword.decode('gbk'), title, detailurl, videourl, upname, apitoken)
    print params
    dbhelper.insert(sql, params)
    value = {
           'table':'bilibili',
           'keyword':keyword.decode('gbk'),
           'title':title,
           'detailurl':detailurl,
           'videourl':videourl,
           'upname':upname,
           'apitoken':apitoken
    }

    lpush('list', json.dumps(value))
    pass

def getsearchpagebykeyword(url, keyword):
    strWd = {"keyword":keyword.decode('gbk')} 
    keyword = urllib.urlencode(strWd)
    strFullurl = url + keyword
    print strFullurl
    return geturlpage(strFullurl)

def geturlpage(url):
    res = requests.get(url)
    return res.text

    proxy = random.choice(proxy_list)
    httpproxy_handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(httpproxy_handler)

    strData = ''
    strHeaders = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    objRequest = urllib2.Request(url = url, headers = strHeaders)
    try:
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
def resolvepagedata(data, keyword, apitoken):
    global num
    num = int(num) + 1
    dbOperator.updateSearchnums((str(num), keyword.decode('gbk'), '哔哩哔哩', apitoken))

    arrList = []
    strRetnexturl = ''
    data=data.encode('utf-8')
    objSoup = BeautifulSoup(data, 'lxml')
    tmpnexturl = objSoup.find_all('li', class_ = 'page-item last')
    objSoup = BeautifulSoup(str(tmpnexturl), 'html.parser')
    tmpnexturl = objSoup.find_all('button', class_ = 'pagination-btn')
    filter = re.compile('>(.*?)<')
    sumstr = filter.findall(str(tmpnexturl))[0].replace('\\\\n', "").strip()
    sum = int(sumstr)
    resolvedetaildata(data, keyword, apitoken)
    return sum

#解析视频播放网页
def resolvedetaildata(data, keyword, apitoken):
    objSoup = BeautifulSoup(data, 'lxml')
    videolist = objSoup.find_all('li', class_ = 'video-item matrix')
    upnamelist = objSoup.find_all('a', class_ = 'up-name')
    for i in range(len(videolist)):
        videoinfo =  str(videolist[i])
        objSoup = BeautifulSoup(videoinfo, 'lxml')
        upnameinfo = str(upnamelist[i])
        filter = re.compile('>(.*?)</a')
        upname = str(filter.findall(upnameinfo)[0])
        detailurl = str(objSoup.find(name='a').get('href'))
        videourl = getrealvideourl(detailurl)
        detailurl = "http:" + str(objSoup.find(name='a').get('href'))
        title = str(objSoup.find(name='a').get('title'))
        insert(keyword, title, detailurl, videourl, upname, apitoken)

    pass
#获取视频实际播放地址//www.bilibili.com/video/av10634999?from=search
def getrealvideourl(detailurl):
    detailurl = "https:" + detailurl.split('.')[0] + ".i" + detailurl[6:]
    res = requests.get(detailurl, allow_redirects=False)
    data = res.text
    filter = re.compile(r'getScript\(\"\S*\"\);')
    apiurl = str(filter.findall(data)[0])
    apiurl = apiurl.replace("getScript(\"", "https:").replace("\"+page+\"", "1").replace("\");", "")
    return apiurl
    strHeaders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                  'Referrer':detailurl,
                  'Upgrade-Insecure-Requests':'0',
                  'Host':'api.bilibili.com',
                  'Connection':'keep-alive',
                  'Accept-Encoding':'gzip, deflate, br',
                  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'}

    res = requests.get(apiurl, headers=strHeaders)
    print res.text
    return videourl

def start_search(keyword, apitoken):
    global num
    data = dbOperator.selectOne((keyword.decode('gbk'), '哔哩哔哩', apitoken))
    dt = datetime.datetime.now()
    timestr = dt.strftime( '%Y-%m-%d %H:%M:%S' )
    print timestr

    if data == None:
        dbOperator.insert(('', '哔哩哔哩', keyword.decode('gbk'), 0, timestr, apitoken))
    else:
        dbOperator.updateSearchtime((timestr, keyword.decode('gbk'), '哔哩哔哩', apitoken))
        num = data[3]
    url = "https://search.bilibili.com/all?"

    keyword = keyword.strip()
    data = getsearchpagebykeyword(url, keyword)

    sum = resolvepagedata(data,keyword, apitoken)
    for i in range(sum + 1):
        if i == 0 or i == 1:
            continue
        strWd = {"keyword":keyword.decode('gbk'),
                 "page":i} 
        urlkeyword = urllib.urlencode(strWd)
        strFullurl = url + urlkeyword
        print strFullurl
        data = geturlpage(strFullurl)
        resolvedetaildata(data, keyword, apitoken)

def main(argv):
    argc = len(argv)
    keyword = ''
    if argc == 1:
        print 'Useage:python bilibili.py {keyword1} {keyword2} ...'
        return
    for i in range(argc):
        if i == 0:
            continue
        keyword = keyword + argv[i] + ' '
    url = "https://search.bilibili.com/all?"

    keyword = keyword.strip()
    data = getsearchpagebykeyword(url, keyword)

    sum = resolvepagedata(data, keyword, test_apitoken)
    for i in range(sum + 1):
        if i == 0 or i == 1:
            continue
        strWd = {"keyword":keyword.decode('gbk'),
                 "page":i} 
        urlkeyword = urllib.urlencode(strWd)
        strFullurl = url + urlkeyword
        print strFullurl
        data = geturlpage(strFullurl)
        resolvedetaildata(data, keyword, test_apitoken)
if __name__ == '__main__':
    main(sys.argv)


    
    