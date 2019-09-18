#coding=utf-8
import execjs
import urllib
import urllib2
import re
import time
import random
import requests
import ssl
import sys
import os
import threading
import datetime
import json
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..")

from videntify.download import *
from bs4 import BeautifulSoup
import socket
socket.setdefaulttimeout(10.0)
from database.opredis import *

num = 0
sys.path.append("..")
from database.searchenginedbHelper import *
from database.dbHelper import *
from database.opredis import *

dbhelper = mySqlHelper()
dbOperator = searchenginedbHelper()
def insert(keyword, title, detailurl, videourl, upname):
    sql = "insert into meipai (keyword, title, detailurl, videourl, upname) values (%s, %s, %s, %s,%s)"
    params = (keyword.decode('gbk'), title, detailurl, videourl, upname)
    print params
    dbhelper.insert(sql, params)

    value = {
           'table':'meipai',
           'keyword':keyword.decode('gbk'),
           'title':title,
           'detailurl':detailurl,
           'videourl':videourl,
           'upname':upname 
    }

    lpush('list', json.dumps(value))
    pass

proxy_list = [
    {"http" : "120.83.110.203:9999"},
    {"http" : "120.83.107.126:9999"},
    {"http" : "182.35.87.208:9999"},
    {"http" : "113.121.21.28:9999"},
    {"http" : "120.83.103.45:9999"}]


def getsearchpagebykeyword(url, keyword):
    strWd = {"q":keyword.decode('gbk')} 
    keyword = urllib.urlencode(strWd)
    strFullurl = url + keyword
    print strFullurl
    return geturlpage(strFullurl)

def geturlpage(url):
    headers = {
        'cookie':'sid=1t483vvh19hve3599vp7t7dmu0; UM_distinctid=16ce17a5f1d18b-021159f97322ff-3b65410e-1fa400-16ce17a5f1e505; virtual_device_id=ce4176a53aef2ca73292e27ad3f9b426; pvid=eSMv8sQSQo6Jin6ZqIorY1WPOh5L5ziJ; searchStr=%E9%92%A2%E9%93%81%E4%BE%A0%7C%E7%BE%8E%E5%9B%BD%E9%98%9F%E9%95%BF%7C; CNZZDATA1256786412=410885764-1567147896-https%253A%252F%252Fwww.baidu.com%252F%7C1567484475; AUTO_LOGIN=1; MUSID=hq2rbechkgojd34uuhoojs1mo6; ASID=00e2ad4cd4349d0cd567e5eba945f160'
    }
    res = requests.get(url, headers = headers)
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

def resolvepagedata(data, keyword):
    global num
    num = int(num) + 1
    dbOperator.updateSearchnums((str(num), keyword.decode('gbk'), '美拍'))

    nextpage = ""
    arrList = []
    strRetnexturl = ''
    data=data.encode('utf-8')
    objSoup = BeautifulSoup(data, 'lxml')
    detailList = objSoup.find_all('a', class_ = 'content-l-p pa')
    upnameList = objSoup.find_all('a', class_ = 'content-name-a js-convert-emoji')
    nextpageList = objSoup.find_all('a', class_ = 'paging-next dbl')
    if len(nextpageList) == 0:
        nextpage = ""
    else:
        nextpage = objSoup.find_all('a', class_ = 'paging-next dbl')[0].get('href')

    print nextpage

    for i in range(len(detailList)):
        detailurl = "https://www.meipai.com/" + detailList[i].get('href')
        videourl = getrealvideourl(detailurl)
        print videourl
        title = detailList[i].get('title')
        upname = upnameList[i].get('title')
        insert(keyword, title, detailurl, videourl, upname)

    return nextpage

def getrealvideourl(detailurl):
    print detailurl
    base64str = ''
    data = geturlpage(detailurl)
    objSoup = BeautifulSoup(data, 'lxml')
    
    if len(objSoup.find_all('meta', property = "og:video:url")) != 0:
        base64str = objSoup.find_all('meta', property = "og:video:url")[0].get("content")  
    elif len(objSoup.find_all('div', class_ = 'detail-media-wrap pr cp')) != 0:
        base64str = objSoup.find_all('div', class_ = 'detail-media-wrap pr cp')[0].get('data-video')
    else:
        base64str = objSoup.find_all('span', class_ = 'detail-share none dbl pr cp')[0].get('data-video')
    
    videourl = js2python(base64str)
    return videourl

def start_search(keyword):
    global num
    data = dbOperator.selectOne((keyword.decode('gbk'), '美拍'))
    dt = datetime.datetime.now()
    timestr = dt.strftime( '%Y-%m-%d %H:%M:%S' )
    print timestr

    if data == None:
        dbOperator.insert(('', '美拍', keyword.decode('gbk'), 0, timestr))
    else:
        dbOperator.updateSearchtime((timestr, keyword.decode('gbk'), '美拍'))
        num = data[3]

    url = "https://www.meipai.com/search/all?"

    data = getsearchpagebykeyword(url, keyword)
    while True:
        nexturl = resolvepagedata(data, keyword)
        if nexturl == "":
            break
        data = geturlpage("https://www.meipai.com" + nexturl)
        
    return

def main(argv):
    argc = len(argv)
    keyword = ''
    if argc == 1:
        print 'Useage:python meipai.py {keyword1} {keyword2} ...'
        return
    for i in range(argc):
        if i == 0:
            continue
        keyword = keyword + argv[i] + ' '
    url = "https://www.meipai.com/search/all?"

    keyword = keyword.strip()
    start_search(keyword)
    return
    data = getsearchpagebykeyword(url, keyword)


    while True:
        nexturl = resolvepagedata(data, keyword)

        data = geturlpage("https://www.meipai.com" + nexturl)
        if nexturl == "":
            break

def js2python(base64str):
    path = ''
    if __name__ == '__main__':
        path = "meipai.js"
    else:
        path = os.getcwd() + "/static/js/meipai.js"
    js = ''
    with open(path,'r') as f:
        js = f.read()

    calljs = execjs.compile(js)
    res = calljs.call('decode', base64str)
    return res


if __name__ == '__main__':
    main(sys.argv)


    
    