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
import json
import base64
import datetime
from urllib import quote
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
from lxml import etree
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
def insert(keyword, title, detailurl, videourl, upname):
    sql = "insert into aiqiyi (keyword, title, detailurl, videourl, upname) values (%s, %s, %s, %s,%s)"
    params = (keyword.decode('gbk'), title, detailurl, videourl, upname)
    print params
    dbhelper.insert(sql, params)

    value = {
           'table':'aiqiyi',
           'keyword':keyword.decode('gbk'),
           'title':title,
           'detailurl':detailurl,
           'videourl':videourl,
           'upname':upname 
    }

    lpush('list', json.dumps(value)) 
    pass

def getsearchpagebykeyword(url, keyword):
    urlkeyword = keyword.decode('gbk')
    strFullurl = url + urlkeyword
    print strFullurl
    return geturlpage(strFullurl)

def resolvepagedata(data, keyword):
    global num
    num = int(num) + 1
    dbOperator.updateSearchnums((str(num), keyword.decode('gbk'), '爱奇艺'))

    arrList = []
    strRetnexturl = ''

    objSoup = BeautifulSoup(data, 'html5lib')
    videoList = objSoup.find_all('li', class_ = 'list_item')

    for i in range(len(videoList)):
        detailurl = videoList[i].a.get('href')
        title = videoList[i].get('data-searchpingback-albumname')
        upname = ""
        videourl = getrealvideourl(detailurl)
        #print title
        if title is None:
            continue
        insert(keyword, title, detailurl, videourl, upname)


    intentList = objSoup.find_all('li', class_ = 'intent-item-twoline')
    
    for i in range(len(intentList)):
        detailurl = intentList[i].div.a.get('href')
        title = intentList[i].div.a.get('title')
        upname = ""
        videourl = getrealvideourl(detailurl)
        print title
        if title is None:
            continue
        insert(keyword, title, detailurl, videourl, upname)

    nextList = objSoup.find_all('a', class_ = 'a1')
    nexturl = ''
    for i in range(len(nextList)):
        if (nextList[i].text == '下一页'):
            nexturl = nextList[i].get('href')

    return nexturl

def getrealvideourl_1(detailurl):
    url = "https://www.administratorv.com/iqiyi/index.php?url=" + detailurl
    data = requests.get(url).text
    filter = re.compile('url=(.*?)\'.split')
    print filter.findall(data)


def getrealvideourl(detailurl):
    print detailurl
    pre_url = "https://www.administratorv.com/iqiyi/index.php?url=" + detailurl
    headers = {
        'Referer': pre_url
    }
    target_url = 'https://www.administratorm.com/ADMIN/index.php?url=' + detailurl
    data = requests.get(target_url, headers=headers).text
    filter = re.compile('referer\':\'(.*?)\',\'ref')
    referer = filter.findall(data)[0]
    print referer
    filter = re.compile('post(.*?),')
    interfaceapi = filter.findall(data)[0]
    interfaceapi = interfaceapi.split('"')[1]

    data = {
         'url':detailurl,
         'referer':referer,
         'ref':'0',
         'time':str(int(time.time() * 1000)),
         'type':'',
         'other':'',
         'ios':''
    }
    headers = {
        'Referer': target_url
    }

    res = requests.post('https://www.administratorm.com/ADMIN/' + interfaceapi, data=data, headers=headers)
    print res.text

    if int(json.loads(res.text)['code']) == 404:
        return json.loads(res.text)['domain']
    if int(json.loads(res.text)['code']) != 200:
        return json.loads(res.text)['url']
    base64videourl = json.loads(res.text)['url']
    print base64videourl
    if base64videourl.find("http") != -1:
        return base64videourl

    videourl = base64.b64decode(base64videourl).replace("%3A", ':').replace("%2F", "/").replace("url=", "")
    if len(videourl.split("http")) == 2:
        videourl = "http" + videourl.split("http")[1]
        print videourl
    return videourl


def geturlpage(url):
    print url
    headers = {
              }
    res = requests.get(url, headers = headers)
    return res.text

def start_search(keyword):
    global num
    data = dbOperator.selectOne((keyword.decode('gbk'), '爱奇艺'))
    dt = datetime.datetime.now()
    timestr = dt.strftime( '%Y-%m-%d %H:%M:%S' )
    print timestr

    if data == None:
        dbOperator.insert(('', '爱奇艺', keyword.decode('gbk'), 0, timestr))
    else:
        dbOperator.updateSearchtime((timestr, keyword.decode('gbk'), '爱奇艺'))
        num = data[3]
    url = 'https://so.iqiyi.com/so/q_'
    data = getsearchpagebykeyword(url, keyword)
    while True:
        nexturl = resolvepagedata(data, keyword)
        if nexturl == "":
            break
        data = geturlpage("https://so.iqiyi.com" + nexturl)
        
    return
    pass

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
    url = "https://so.iqiyi.com/so/q_"

    keyword = keyword.strip()

    data = getsearchpagebykeyword(url, keyword)


    while True:
        nexturl = resolvepagedata(data, keyword)
        data = geturlpage("https://so.iqiyi.com" + nexturl)
        if nexturl == "":
            break
if __name__ == '__main__':
    #http://www.wmxz.wang/video.php?url=http://so.iqiyi.com/links/qcAdm6fzqd2Da5AHK1fa8AjE_pjgrwo30uShwvURIkLJ0Ni0R408WwrZ4x5P4VmPz-C4MMuvGYwiF-rMlitQfg==
    #print getrealvideourl('http://so.iqiyi.com/links/qcAdm6fzqd2Da5AHK1fa8AjE_pjgrwo30uShwvURIkLJ0Ni0R408WwrZ4x5P4VmPz-C4MMuvGYwiF-rMlitQfg==')
    #print getrealvideourl_1('http://so.iqiyi.com/links/qcAdm6fzqd2Da5AHK1fa8AjE_pjgrwo30uShwvURIkLJ0Ni0R408WwrZ4x5P4VmPz-C4MMuvGYwiF-rMlitQfg==')
    #start_search('钢铁侠'.encode('gbk'))
    main(sys.argv)