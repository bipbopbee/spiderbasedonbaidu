#coding=utf-8
import os
import datetime
import traceback
import subprocess
import tempfile
import sys
import threading
from curl2python import *
import json
import pymysql
import time
headers = {"Authorization":"LWtrKgMmLIeAWyyDUlLa"}
conn = pymysql.connect(
    host = '127.0.0.1',user = 'root',passwd = '123456',
    port = 3306,db = 'videoright',charset = 'utf8'
    #port必须写int类型
    #charset必须写utf8，不能写utf-8
)
cursor = conn.cursor()
url = "https://zy.zxziyuan-yun.com/20180107/hv8I41wD/index.m3u8"
name = "tmp.mp4"
#ffmpeg -i "https://zy.zxziyuan-yun.com/20180107/hv8I41wD/index.m3u8" -vcodec copy -acodec copy -absf aac_adtstoasc output.mp4
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

def fingerprint_query(hosturl, detailurl, desc72file, headers):
    jobidstr = asyncquerylocalfile(desc72file, headers)
    print jobidstr
    jobid = json.loads(jobidstr)['data']['job']['id']
    t = threading.Thread(target = threading_jobquey, args=(hosturl, detailurl, headers, jobid))
    t.start()
    #等待线程结束
    t.join()
    pass

def desc72_generate(filename):
    try:
        command = "desc_tools " +  filename + " " + filename + ".desc72"
        outtemp =tempfile.SpooledTemporaryFile(bufsize = 100 * 1000)
        fileno = outtemp.fileno()
        fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=False)
        fd.communicate()
        # outtemp.seek(0)
        # lines = outtemp.readlines()
        # print lines
    except Exception, e:
        print traceback.format_exc()
    finally:
        if outtemp:
            outtemp.close()

def thread_download(detailurl, url, nowtime):
    try:
        command = "ffmpeg -i " + url + " -vcodec copy -acodec copy -absf aac_adtstoasc " + nowtime + ".mp4"
        outtemp =tempfile.SpooledTemporaryFile(bufsize = 100 * 1000)
        fileno = outtemp.fileno()
        fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=False)
        fd.communicate()
        #outtemp.seek(0)
        #lines = outtemp.readlines()
        #print linesse
    except Exception, e:
        print traceback.format_exc()
    finally:
        if outtemp:
            outtemp.close()

    if os.path.exists(nowtime + ".mp4"):
        desc72_generate(nowtime + ".mp4")
        os.remove(nowtime + ".mp4")
        fingerprint_query(detailurl, url,  nowtime + ".mp4" + ".desc72", headers)

if __name__ == "__main__":
    nowtime = str(datetime.datetime.now().microsecond)
    print nowtime
    detailurl = 'http://www.bilibili.com/video/av20169226?from=search'
    videourl = 'https://api.bilibili.com/playurl?callback=callbackfunction&aid=51585747&page=1&platform=html5&quality=1&vtype=mp4&type=jsonp'
    t = threading.Thread(target=thread_download, args=(detailurl, videourl, nowtime))
    t.start()
    #fingerprint_query("www.baidu.com", url, "21000.mp4.desc72", headers)
    pass