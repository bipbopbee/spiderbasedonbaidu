#coding=utf-8
import json
import sys
import datetime
import time
import threading
import uuid
from download import *
sys.path.append("..")
from database.opredis import *
from database.dbHelper import *
from database.searchenginedbHelper import *
dbhelper = mySqlHelper()
dbOperator = searchenginedbHelper()

thread_num = 10

#     table:
#     keyword:
#     title:
#     detailurl:
#     videourl:
#     upname:

def thread_function(keystr):
    while True:
        value = rpop(keystr)
        if value == None:
            time.sleep(5)
            continue
        data = json.loads(value)
        print data
        hosturl = data['detailurl']
        videourl = data['videourl']
        #nowtime = str(datetime.datetime.now().microsecond)
        filename = str(uuidsed.uuid1())
        thread_download(hosturl, videourl, filename)
    pass

if __name__ == '__main__':
    for i in range(thread_num):
        t = threading.Thread(target=thread_function, args=(key,))
        t.start()