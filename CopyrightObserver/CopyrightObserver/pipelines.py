# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys
import threading
import pymysql
sys.path.append("../../..")
from videntify.curl2python import *
from videntify.download import *
import datetime
#headers = {"Authorization":"LWtrKgMmLIeAWyyDUlLa"}
headers = {}
conn = pymysql.connect(
    host = '127.0.0.1',user = 'root',passwd = '123456',
    port = 3306,db = 'videoright',charset = 'utf8'
    #port必须写int类型
    #charset必须写utf8，不能写utf-8
)
cursor = conn.cursor()
class CopyrightobserverPipeline(object):
    def __init__(self):
        self.file = open('result.json','wb')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.encode('utf-8'))
        apitoken = item['apitoken']
        headers = {"Authorization": apitoken}
        detailurl = item['detailurl']
        videourl = item['videourl']
        if videourl[-4:] == "m3u8" or videourl[-4:] == "M3U8":
            nowtime = str(datetime.datetime.now().microsecond)
            t = threading.Thread(target=thread_download, args=(detailurl, videourl, nowtime))
            t.start()
            return item
        jobidstr = asyncqueryurl(item['videourl'], headers)
        jobid = json.loads(jobidstr)['data']['job']['id']
        t = threading.Thread(target = threading_jobquey, args=(detailurl, videourl, headers, jobid))
        t.start()
        return item

def threading_jobquey(hosturl, detailurl, headers, jobid):
    while True:
        try:
            statusstr = queryjobstatus(jobid, headers = headers)
        except requests.exceptions.ConnectionError:
            print "error"
        status = json.loads(statusstr)['data']['job']['status']
        if status == 'success':
            print 'success'
            link = json.loads(statusstr)['data']['job']['result_url']
            matchesttr = querypersistedresult(link, headers)
            print matchesttr
            matches = json.loads(matchesttr)['data']['matches']
            print len(matches)
            i = 0
            contentid = ':'
            for i in range(len(matches)):
                contentid = contentid + matches[i]['content']['content_id'] + ":"
                print contentid

            if len(matches) > 0:
                first_contentid = contentid.split(":")[1]
                print first_contentid
                sql = "select * from right_tmp where contentid = \'" + first_contentid + "\';"
                cursor.execute(sql)
                row = cursor.fetchone()
                rightname = row[2]

                sql = "insert into privacy (url, rightname, contentid, hosturl) values (\'"
                sql = sql + detailurl + "\', \'" + rightname + "\', \'" + first_contentid + "\',\'" + hosturl + "\')"
                print sql
                cursor.execute(sql)
                conn.commit()
            break
        elif status == 'error':
            break
        elif status == 'cancelled':
            break
    pass