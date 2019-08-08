#coding=utf-8
import urllib
import urllib2
import re
import time
#from SpiderLogger import logger
#from csimulate import getLineFileFunc
#解决utf8 code问题
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json


#网盘未登录时bdstoken为null
bdstoken = '114e65f042d6b2d78bdc024cac84818a'
stoken ="72641e1ffa306dffd63b87dc5c2a2d7b20d79b19dff9dec94f7ee05a1cefd8da"
bduss = "ZQV2lDd3JMbmsyUHkxQ0pvSjA0TGdDdjMxUlZsNE1vUUIzfjlWWWZZUFcwSEJkSUFBQUFBJCQAAAAAAAAAAAEAAAAyWqQ2use6x7TzMjMxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANZDSV3WQ0ldcn"
def init(bduss, stoken, referer):
    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, defalte, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Connection-Length':'161',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'BDUSS=%s;STOKEN=%s;' %(bduss, stoken),
        'Host': 'pan.baidu.com',
        'Referer': referer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'X-Requested-With': 'XMLHttpRequest'
    }
    return headers
#{"查询字符串":{"shareid":"1271301197","from":"196432005","ondup":"newcopy","async":"1","channel":"chunlei","web":"1","app_id":"250528","bdstoken":"114e65f042d6b2d78bdc024cac84818a","logid":"MTU2NTE0MjYzNjg3NTAuNjE5NTE5MjYzMzAxNzAyOQ==","clienttype":"0"},"表单数据":{"fsidlist":"[1097759823772592]","path":"/"}}
#https://pan.baidu.com/share/transfer?shareid=1271301197&from=196432005&ondup=newcopy&async=1&channel=chunlei&web=1&app_id=250528&bdstoken=114e65f042d6b2d78bdc024cac84818a&logid=MTU2NTE0MjYzNjg3NTAuNjE5NTE5MjYzMzAxNzAyOQ==&clienttype=0
def transfer(shareid, _from, bdstoken, fsidlist, path, headers):
    ondup = "newcopy"
    async = "1"
    channel = "chunlei"
    clienttype = "0"
    web = "1"
    app_id = "250528"
    logid = "MTU2NTE0MjYzNjg3NTAuNjE5NTE5MjYzMzAxNzAyOQ=="

    url_trans = "https://pan.baidu.com/share/transfer?shareid=%s" \
                "&from=%s" \
                "&ondup=%s" \
                "&async=%s" \
                "&channel=%s" \
                "&web=%s" \
                "&app_id=%s" \
                "&bdstoken=%s" \
                "&logid=%s"     \
                "&clienttype=%s" % (shareid, _from, ondup, async, channel, web, app_id, bdstoken, logid, clienttype)
    #"表单数据":{"fsidlist":"[1097759823772592]","path":"/"}
    form_data = {
        "fsidlist":fsidlist,
        "path":path
    }

    response = requests.post(url_trans, data = form_data, headers = headers, verify=False)
    print response.content
    jsob = json.loads(response.content)
    
    if "errno" in jsob:
        return jsob["errno"]
    else:
        return None

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

#@return 返回参数
def resolvepagedata(data):
    pattern1 = re.compile(r'yunData.SHARE_ID = \S*\;')
    pattern2 = re.compile(r'yunData.SHARE_UK = \S*\;')
    pattern3 = re.compile(r'yunData.FS_ID = \S*\;')
    #pattern4 = re.compile(r'\"bdstoken\":\"(.*?)\\\"')
    shareid  = pattern1.findall(data)[0]
    _from = pattern2.findall(data)[0]
    fsidlist = pattern3.findall(data)[0]
    #bdstoken = pattern4.findall(data)[0]
    pattern4 = re.compile('\"(.*?)\"')
    shareid = pattern4.findall(shareid)[0]
    _from = pattern4.findall(_from)[0]
    fsidlist = pattern4.findall(fsidlist)[0]
    fsidlist = "[" + fsidlist + "]"
    return (shareid, _from, fsidlist)

if __name__ == "__main__":
    url = "https://pan.baidu.com/s/1bZUp9CdQWpWt1aH3Pc8TrQ"
    data = geturlpage(url)
    # f = open("wangpan.html","w")
    # f.write(data)
    # f.close()
    shareid, _from, fsidlist = resolvepagedata(data)

    headers = init(bduss, stoken, url)
    transfer(shareid, _from, bdstoken, fsidlist, "/", headers)