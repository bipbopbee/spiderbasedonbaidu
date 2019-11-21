#coding=utf-8
import execjs
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
import base64
from urllib import quote
from urllib import unquote
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
from lxml import etree
import socket
socket.setdefaulttimeout(10.0)
from opredis import lpush
dbnum = 0
sys.path.append("..")
from database.dbHelper import *
from database.searchenginedbHelper import *
from database.opredis import *
dbhelper = mySqlHelper()
dbOperator = searchenginedbHelper()
test_apitoken = ""
def insert(keyword, title, detailurl, videourl, upname, apitoken):
    sql = "insert ignore into tengxun (keyword, title, detailurl, videourl, upname, apitoken) values (%s, %s, %s, %s,%s,%s)"
    params = (keyword.decode('gbk'), title, detailurl, videourl, upname, apitoken)
    print params
    dbhelper.insert(sql, params)

    value = {
           'table':'tengxun',
           'keyword':keyword.decode('gbk'),
           'title':title,
           'detailurl':detailurl,
           'videourl':videourl,
           'upname':upname,
           'apitoken':apitoken
    }
    #print requests.post('http://118.31.127.81:5000/appium/upload', value)
    lpush('list', json.dumps(value))
    pass

num = 1

def getsearchpagebykeyword(url, keyword):
    global num
    strWd = {"last_query":keyword.decode('gbk'),
             "qid":"5zEE1iA6bHP3lzTSvAR2mPK58bTMCGEdy9eChXsuW-jvGUnm36N-hQ",
             "tabid_list":"0|17|7|4|106|1|2|3|11|6|12|21|14|5|8|13|15|20|1100",
             "tabname_list":"全部|游戏|其他|动漫|少儿|电影|电视剧|综艺|新闻|纪录片|娱乐|汽车|体育|音乐|原创|财经|教育|母婴|知识",
             "resolution_tabid_list":"0|1|2|3|4|5",
             "resolution_tabname_list":"全部|标清|高清|超清|蓝光|VR",
             "q":keyword.decode("gbk"),
             "stag":3,
             "needCorrect":keyword.decode("gbk"),
             "cur":num,
             "cxt":"tabid=0&sort=0&pubfilter=0&duration=0"
            } 
    keyword = urllib.urlencode(strWd)
    strFullurl = url + keyword
    return geturlpage(strFullurl)


def resolvepagedata(data, keyword, apitoken):
    global dbnum
    global num
    dbnum = int(dbnum) + 1
    dbOperator.updateSearchnums((str(dbnum), keyword.decode('gbk'), '腾讯', apitoken))
    arrList = []
    strRetnexturl = ''
    objSoup = BeautifulSoup(data, 'html5lib')
    videoList = objSoup.find_all('div', class_ = 'result_item result_item_h _quickopen')
    print len(videoList)
    for i in range(len(videoList)):
        detailurl = videoList[i].a.get('href')
        print detailurl
        title = ""
        title = videoList[i].find_all('h2', class_ = 'result_title')[0].find_all('a')[0].text
        print title
        upname = ""
        upname = videoList[i].find_all('div', class_ = 'info_item info_item_even')
        if len(upname) != 0 and upname[0].a != None:
            upname = upname[0].a.text
        else:
            upname = ''
        print upname
        videourl = getrealvideourl(detailurl)
        print videourl
        insert(keyword, title, detailurl, videourl, upname, apitoken)
    
    intentList = objSoup.find_all('div', class_ = 'mod_figures mod_figure_v')
    if len(intentList) != 0:
        itemlist = intentList[0].find_all('li', class_ = 'list_item')
        for m in range(len(itemlist)):
            detailurl = itemlist[m].find_all('strong', class_ = 'figure_title figure_title_two_row')[0].a.get('href')
            print detailurl
            title = itemlist[m].find_all('strong', class_ = 'figure_title figure_title_two_row')[0].a.get('title')
            print title
            upname = ""
            videourl = getrealvideourl_1(detailurl)
            print videourl
            insert(keyword, title, detailurl, videourl, upname, apitoken)

    num = num + 1

def getrealvideourl_1(detailurl):
    url = "https://www.administratorv.com/qqvod/index.php?url=" + detailurl
    data = requests.get(url).text
    filter = re.compile('url=(.*?)\'.split')
    if len(filter.findall(data)) > 0:
        videourl = filter.findall(data)[0]
        return videourl
    else:
        return ''

def getrealvideourl(detailurl):
    print detailurl
    pre_url = "https://www.administratorv.com/qqvod/index.php?url=" + detailurl
    headers = {
        'Referer': pre_url
    }
    target_url = 'https://www.administratorm.com/ADMIN/index.php?url=' + detailurl
    data = requests.get(target_url, headers=headers).text

    filter = re.compile('referer\':\'(.*?)\',\'ref')
    referer = filter.findall(data)[0]

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

    if int(json.loads(res.text)['code']) == 404:
        return json.loads(res.text)['domain']
    if int(json.loads(res.text)['code']) != 200:
        return json.loads(res.text)['url']
    base64videourl = json.loads(res.text)['url']

    lasturl = base64.b64decode(base64videourl)[3:]
    headers = {
        'Referer': target_url
    }

    if lasturl.find('url=') != -1:
        lasturl = lasturl.replace("%3A", ':').replace("%2F", "/")
        lasturl =  lasturl.split("url=")[1]
        return lasturl
    res = requests.get(lasturl,headers = headers)
    jsonStr = json.loads(res.text)

    vlJson = json.loads(jsonStr['vinfo'])
    if vlJson.has_key('vl'):
        vlJson = vlJson['vl']
    else:
        return lasturl
    videourl = ''
    videourl = vlJson['vi'][0]['ul']['ui'][0]['url'] + vlJson['vi'][0]['fn'] + "?vkey=" + vlJson['vi'][0]['fvkey']

    return videourl


def geturlpage(url):
    headers = { 
              }
    res = requests.get(url, headers = headers)
    return res.text

def start_search(keyword, apitoken):
    global num
    global dbnum
    data = dbOperator.selectOne((keyword.decode('gbk'), '腾讯', apitoken))
    dt = datetime.datetime.now()
    timestr = dt.strftime( '%Y-%m-%d %H:%M:%S' )
    print timestr

    if data == None:
        dbOperator.insert(('', '腾讯', keyword.decode('gbk'), 0, timestr, apitoken))
    else:
        dbOperator.updateSearchtime((timestr, keyword.decode('gbk'), '腾讯', apitoken))
        dbnum = data[3]
    url = "https://v.qq.com/x/search/?ses="
    while True:
        data = getsearchpagebykeyword(url, keyword)
        resolvepagedata(data, keyword, apitoken)
        if num == 20:
            break
        
    return
    pass

def main(argv):
    global num
    argc = len(argv)
    keyword = ''
    if argc == 1:
        print 'Useage:python tengxun.py {keyword1} {keyword2} ...'
        return
    for i in range(argc):
        if i == 0:
            continue
        keyword = keyword + argv[i] + ' '
    url = "https://v.qq.com/x/search/?ses="
    keyword = keyword.strip()


    while True:
        data = getsearchpagebykeyword(url, keyword)
        resolvepagedata(data, keyword, test_apitoken)
        if num == 20:
            break

if __name__ == '__main__':
    main(sys.argv)
    #print getrealvideourl('https://v.qq.com/x/page/s0865l5taij.html')