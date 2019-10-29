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
sys.path.append("..")
from searchengines.tengxun import start_search as tengxun_search
import threading
# http://118.31.127.81:5000/profile/getall
# http://118.31.127.81:5000/appium/upload
def geturlpage(url):
    headers = { 
              }
    res = requests.get(url, headers = headers)
    return res.text
if __name__ == '__main__':
    res = geturlpage('http://118.31.127.81:5000/profile/getall')
    jsonData = json.loads(res)['data']
    for m in range(len(jsonData)):
        tengxun_search(jsonData[m]['rightname'].encode('gbk'))
        # t = threading.Thread(target=tengxun_search, args=(jsonData[m]['rightname'].encode('gbk'),))
        # t.start()