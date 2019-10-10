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
from urllib import unquote
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
from lxml import etree
import socket
socket.setdefaulttimeout(10.0)
from opredis import lpush
num = 0
sys.path.append("..")
from database.searchenginedbHelper import *
from database.dbHelper import *
from database.opredis import *
dbhelper = mySqlHelper()
dbOperator = searchenginedbHelper()
def insert(keyword, title, detailurl, videourl, upname):
    sql = "insert into youku (keyword, title, detailurl, videourl, upname) values (%s, %s, %s, %s,%s)"
    params = (keyword.decode('gbk'), title, detailurl, videourl, upname)
    print params
    dbhelper.insert(sql, params)

    value = {
           'table':'youku',
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
    dbOperator.updateSearchnums((str(num), keyword.decode('gbk'), '优酷'))
    contentdata = ''
    filter = re.compile('bigview.view\({(.*?)}\)')
    htmlList = filter.findall(data)
    print len(htmlList)
    if len(htmlList) != 0:
        contentdata = htmlList[0].split('"html":')[1]
        contentdata = contentdata.replace('\\n', "").replace("\\t", "").replace("\\\"", "\"")
    arrList = []
    strRetnexturl = ''
    objSoup = BeautifulSoup(contentdata, 'html5lib')
    videoList = objSoup.find_all('div', class_ = 'sk-mod')
    print len(videoList) 
    for i in range(len(videoList) - 1):
        detailurl = videoList[i].find_all('div', class_ = 'mod-main')[0].div.a.get('href')
        print detailurl
        videourl = getrealvideourl_1(detailurl)
        if videourl.find('m3u8') == -1:
            videourl = getrealvideourl(detailurl)
        print videourl

        title = videoList[i].find_all('div', class_ = 'mod-main')[0].div.a.text
        print title

        upname = ''
        upname = videoList[i].find_all('div', class_ = 'mod-main')[0].find_all('div', class_ = 'mod-info')[0].a.text
        print upname

        insert(keyword, title, detailurl, videourl, upname)
    nexturl = ''
    nextList = objSoup.find_all('li', class_ = 'next')
    if (len(nextList) > 0):
        if nextList[0].a != None:
            nexturl = nextList[0].a.get('href')
    print nexturl
    return nexturl

def getrealvideourl_1(detailurl):
    url = "https://www.administratorv.com/youku/index.php?url=" + detailurl
    data = requests.get(url).text
    filter = re.compile('url=(.*?)\'.split')
    videourl = filter.findall(data)[0]
    return videourl
def getrealvideourl(detailurl):
    print detailurl
    pre_url = "https://www.administratorv.com/youku/index.php?url=" + detailurl
    headers = {
        'Referer': pre_url
    }
    target_url = 'https://www.administratorm.com/ADMIN/index.php?url=' + detailurl
    data = requests.get(target_url, headers=headers).text
    filter = re.compile('referer\':\'(.*?)\',\'ref')
    referer = filter.findall(data)[0]
    print referer

    data = {
         'url':detailurl,
         'referer':referer,
         'ref':'0',
         'time':str(int(time.time() * 1000)),
         'type':'',
         'ios':''
    }
    headers = {
        'Referer': target_url
    }
    res = requests.post('https://www.administratorm.com/ADMIN/api.php', data=data, headers=headers)
    print res.text

    if json.loads(res.text).has_key('code'):
        if int(json.loads(res.text)['code']) == 404:
            return json.loads(res.text)['domain']
        if int(json.loads(res.text)['code']) != 200:
            return json.loads(res.text)['url']
        base64videourl = json.loads(res.text)['url']
        print base64videourl
        videourl = base64.b64decode(base64videourl)[3:]
        if videourl.find(".m3u8") != -1:
            return videourl
        videourl = unquote(unquote(unquote(base64.b64decode(base64videourl)))[3:])
        videourl =  videourl.split("url=")[1]
        return videourl
    else:
        return detailurl
    


def geturlpage(url):
    print url
    headers = { 'Cookie': \
	'__ysuid=1561711991387Bpe;' \
	'UM_distinctid=16ce1621e9b83c-06efd3247a7c62-3b65410e-1fa400-16ce1621e9c823;' \
	'cna=SCKaFchUAXUCATFKQAkpCqqQ;' \
	'__aysid=1568012328437l2P;' \
	'_uab_collina=156801235184163338855484;' \
	'juid=01dkad3lnv1rag;' \
	'_m_h5_tk=8c2a1f52fe302cf91bfe77211632077e_1568016319962;' \
	'_m_h5_tk_enc=9d6305bd71d0df8bc4c37e091afaa14b;' \
	'yseidcount=1;' \
	'ysestep=2;' \
	'ystep=2;' \
	'__aysvstp=6;' \
	'ctoken=KRECGeOtHO9bEXxK9L07TJqN;' \
	'__ayft=1568014472956;' \
	'__arpvid=1568014472956NDhArO-1568014472974;' \
	'__ayscnt=1;' \
	'__aypstp=1;' \
	'__ayspstp=7;' \
	'CNZZDATA1277958921=61691630-1568008804-https%253A%252F%252Fyouku.com%252F%7C1568014204;' \
	'P_ck_ctl=EC78DDE4D4914375F0BBF93CCFE19958;' \
	'isg=BLy8zylDzTmS-vl7i3Tpc3M0jVquHWNai-KHTJY9IKeKYVrrvsHjb5OTRcm8KZg3;'
              }
    res = requests.get(url, headers = headers)
    return res.text

def start_search(keyword):
    global num
    data = dbOperator.selectOne((keyword.decode('gbk'), '优酷'))
    dt = datetime.datetime.now()
    timestr = dt.strftime( '%Y-%m-%d %H:%M:%S' )
    print timestr

    if data == None:
        dbOperator.insert(('', '优酷', keyword.decode('gbk'), 0, timestr))
    else:
        dbOperator.updateSearchtime((timestr, keyword.decode('gbk'), '优酷'))
        num = data[3]

    url = 'https://so.youku.com/search_video/q_'
    data = getsearchpagebykeyword(url, keyword)
    while True:
        nexturl = resolvepagedata(data, keyword)
        if nexturl == "":
            break
        data = geturlpage("https://so.youku.com" + nexturl)
        
    return


def main(argv):
    argc = len(argv)
    keyword = ''
    if argc == 1:
        print 'Useage:python youku.py {keyword1} {keyword2} ...'
        return
    for i in range(argc):
        if i == 0:
            continue
        keyword = keyword + argv[i] + ' '
    url = "https://so.youku.com/search_video/q_"
    keyword = keyword.strip()
    data = getsearchpagebykeyword(url, keyword)


    while True:
        nexturl = resolvepagedata(data, keyword)
        data = geturlpage("https://so.youku.com" + nexturl)
        if nexturl == "":
            break
if __name__ == '__main__':
    start_search('钢铁侠'.encode('gbk'))
    #main(sys.argv)