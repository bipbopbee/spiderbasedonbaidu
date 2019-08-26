#coding=utf-8
import urllib
import urllib2
import re
import time
import threading
from datetime import datetime
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

dblock = threading.Lock()
import pymysql
conn = pymysql.connect(
    host = '127.0.0.1',user = 'root',passwd = '123456',
    port = 3306,db = 'videoright',charset = 'utf8'
    #port必须写int类型
    #charset必须写utf8，不能写utf-8
)
cursor = conn.cursor()

def getsearchpagebykeyword(url, keyword):
    strWd = {'wd':keyword}
    strWd = urllib.urlencode(strWd)
    strFullurl = url + strWd
    return geturlpage(strFullurl)

def geturlpage(url):
    strData = ''
    strHeaders = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    objRequest = urllib2.Request(url = url, headers = strHeaders)
    try:
        objResponse = urllib2.urlopen(objRequest, data = None, timeout = 5)
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
    #print tmpnexturl
    pattern = re.compile('\"(.*?rsv_page=1)\"')
    if (len(pattern.findall(data)) == 0):
        strRetnexturl = ""
        return (arrList, strRetnexturl)
    tmpnexturl = pattern.findall(data)[0].split("href=")
    tmpnexturl = tmpnexturl[len(tmpnexturl) - 1]
    print tmpnexturl[1:]
    if tmpnexturl:
        strRetnexturl = tmpnexturl[1:]
    for link in objSoup.find_all(name='a', attrs={'href':re.compile(r'^http:')}):
        arrList.append(link.get('href'))
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
    cursor = conn.cursor()
    num = 0
    dblock.acquire()
    cursor.execute("select * from searchengine where keyword = \'" + keyword + "\'")
    collection = cursor.fetchall()
    cursor.close()
    dblock.release()

    dt = datetime.now()
    timestr = dt.strftime( '%Y-%m-%d %H:%M:%S' )
    print timestr

    if len(collection) == 0:
        cursor = conn.cursor()
        num = 0
        sql = "insert into searchengine (id, name, keyword, searchnums, searchtime)  values (NULL, '百度', \'" + keyword +"\','0\',\'" + timestr + "\');"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
    else:
        sql = "update searchengine set searchtime=\'" + timestr + "\' where keyword=\'" + keyword + "\';"
        print sql
        dblock.acquire()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        dblock.release()
        num = collection[0][3]
        print num

    url = "http://www.baidu.com/s?"
    #searchcount = 50
    #n = 0
    data = getsearchpagebykeyword(url, keyword)
    while True:
        websiteslist, nexturl = resolvepagedata(data)
        for website in websiteslist:
            #print getvideoadress(website)
            num = int(num) + 1
            sql = "update searchengine set searchnums=\'" + str(num) + "\' where keyword=\'" + keyword + "\';"
            print sql
            
            dblock.acquire()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            dblock.release()
            lpush('myspider:start_urls', website)
        data = geturlpage(url[:-3] + nexturl)
        if nexturl == "":
            break
    return
        #n = n + 1
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
    #searchcount = 50
    #n = 0
    data = getsearchpagebykeyword(url, keyword)

    keyword = u'急速追杀'
    num = 0
    cursor.execute("select * from searchengine where keyword = \'" + keyword + "\'")
    collection = cursor.fetchall()
    
    if len(collection) == 0:
        num = 0
        sql = "insert into searchengine (id, name, keyword, searchnums)  values (NULL, '百度', \'" + keyword +"\','0');"
        cursor.execute(sql)
        conn.commit()
    else:
        num = collection[0][3]
        print num
    
    while True:
        websiteslist, nexturl = resolvepagedata(data)
        for website in websiteslist:
            print getvideoadress(website)
            num = int(num) + 1
            sql = "update searchengine set searchnums=\'" + str(num) + "\' where keyword=\'" + keyword + "\';"
            print sql
            cursor.execute(sql)
            conn.commit()
            #lpush('myspider:start_urls', website)
        data = geturlpage(url[:-3] + nexturl)
        print url[:-3] + nexturl
        if nexturl == "":
            break
        #n = n + 1
if __name__ == '__main__':
    main(sys.argv)


    
    