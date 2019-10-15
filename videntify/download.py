#coding=utf-8
import os
import datetime
import traceback
import subprocess
import tempfile
import sys
import threading
from curl2python import *
sys.path.append("..")
from database.config import *
import json
import pymysql
import time
import uuid as uuidsed
import platform
headers = {"Authorization":"LWtrKgMmLIeAWyyDUlLa"}
# conn = pymysql.connect(
#     host = '127.0.0.1',user = 'root',passwd = '123456',
#     port = 3306,db = 'videoright',charset = 'utf8'
#     #port必须写int类型
#     #charset必须写utf8，不能写utf-8
# )
conn = pool.connection()
cursor = conn.cursor()
url = "https://zy.zxziyuan-yun.com/20180107/hv8I41wD/index.m3u8"
hosturl = "www.baidu.com"
name = "tmp.mp4"
#ffmpeg -i "https://zy.zxziyuan-yun.com/20180107/hv8I41wD/index.m3u8" -vcodec copy -acodec copy -absf aac_adtstoasc output.mp4
def threading_jobquey(hosturl, detailurl, headers, jobid, desc72file):
    while True:
        try:
            statusstr = queryjobstatus(jobid, headers = headers)
            print statusstr
        except requests.exceptions.ConnectionError:
            print "error"
            return
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
    os.remove(desc72file)
    pass

def fingerprint_query(hosturl, detailurl, desc72file, headers):
    jobidstr = asyncquerylocalfile(desc72file, headers)
    print jobidstr
    jobid = json.loads(jobidstr)['data']['job']['id']
    t = threading.Thread(target = threading_jobquey, args=(hosturl, detailurl, headers, jobid, desc72file))
    t.start()
    #等待线程结束
    #t.join()
    #os.remove(desc72file)
    pass

def desc72_generate(filename):
    command = "desc_tools " +  filename + " " + filename + ".desc72"
    sysstr = platform.system()
    try:
        outtemp =tempfile.SpooledTemporaryFile(bufsize = 100 * 1000)
        fileno = outtemp.fileno()
        if sysstr == 'Windows':
            fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=False)
        else:
            fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=True)
        fd.communicate()
            # outtemp.seek(0)
            # lines = outtemp.readlines()
            # print lines
    except Exception, e:
        print traceback.format_exc()
    finally:
        if outtemp:
            outtemp.close()


def thread_download(detailurl, url, uuid):
    command = "ffmpeg -i " + url + " -vcodec copy -acodec copy -absf aac_adtstoasc " + uuid + ".mp4"
    sysstr = platform.system()
    try:
        outtemp =tempfile.SpooledTemporaryFile(bufsize = 100 * 1000)
        fileno = outtemp.fileno()
        if sysstr == 'Windows':
            fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=False)
        else:
            fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=True)
        fd.communicate()
            #outtemp.seek(0)
            #lines = outtemp.readlines()
            #print linesse
    except Exception, e:
        print traceback.format_exc()
    finally:
        if outtemp:
            outtemp.close()

    if os.path.exists(uuid + ".mp4"):
        desc72_generate(uuid + ".mp4")
        os.remove(uuid + ".mp4")
        fingerprint_query(detailurl, url,  uuid + ".mp4" + ".desc72", headers)

if __name__ == "__main__":
    uuid = uuidsed.uuid1()
    print uuid
    # return
    # nowtime = str(datetime.datetime.now().microsecond)
    # print nowtime
    detailurl = 'https://www.meipai.com//media/1133082612'
    videourl = 'https://mvvideo10.meitudata.com/5d3ae8205d546gsezfbop15152_H264_1_a099c2aebd96e0.mp4'
    t = threading.Thread(target=thread_download, args=(detailurl, videourl, str(uuid)))
    t.start()
    #fingerprint_query("www.baidu.com", url, "rionman1.mkv.desc72", headers)
    # pass