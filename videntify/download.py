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
headers = {"Authorization":"LWtrKgMmLIeAWyyDUlLa"}
conn = pymysql.connect(
    host = '127.0.0.1',user = 'root',passwd = '123456',
    port = 3306,db = 'videoright',charset = 'utf8'
    #port必须写int类型
    #charset必须写utf8，不能写utf-8
)
url = "https://zy.zxziyuan-yun.com/20180107/hv8I41wD/index.m3u8"
name = "tmp.mp4"
#ffmpeg -i "https://zy.zxziyuan-yun.com/20180107/hv8I41wD/index.m3u8" -vcodec copy -acodec copy -absf aac_adtstoasc output.mp4


def threading_jobquey(detailurl, headers, jobid):
    while True:
        statusstr = queryjobstatus(jobid, headers = headers)
        status = json.loads(statusstr)['data']['job']['status']
        if status == 'finished':
            link = json.loads(statusstr)['data']['job']['result_url']
            matchesttr = querypersistedresult(link, headers)
            matches = json.loads(matchesttr)['data']['matches']
            i = 0
            contentid = ':'
            for i in range(len(matches)):
                contentid = contentid + matches[i]['content']['content_id'] + ":"
            break
            if len(matches) > 0:
                sql = "insert into privacy (url, privacyname, contentid) values ("
                sql = sql + detailurl + "，" + "  ," + contentid + ")"
                cursor.execute(sql)
                conn.commit()
            break
        elif status == 'error':
            break
        elif status == 'cancelled':
            break
    pass

def fingerprint_query(detailurl, desc72file, headers):
    jobidstr = asyncquerylocalfile(desc72file, headers)
    print jobidstr
    jobid = json.loads(jobidstr)['data']['job']['id']
    t = threading.Thread(target = threading_jobquey, args=(detailurl, headers, jobid))
    t.start()
    pass

def desc72_generate(filename):
    try:
        command = "desc_tools " +  filename + " " + filename + ".desc72"
        outtemp =tempfile.SpooledTemporaryFile(bufsize = 10 * 1000)
        fileno = outtemp.fileno()
        fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=False)
        fd.wait()
        outtemp.seek(0)
        lines = outtemp.readlines()
        print lines
    except Exception, e:
        print traceback.format_exc()
    finally:
        if outtemp:
            outtemp.close()

def thread_download(detailurl, url, nowtime):
    try:
        command = "ffmpeg -i " + url + " -vcodec copy -acodec copy -absf aac_adtstoasc " + nowtime + ".mp4"
        outtemp =tempfile.SpooledTemporaryFile(bufsize = 10 * 1000)
        fileno = outtemp.fileno()
        fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=False)
        fd.wait()
        outtemp.seek(0)
        lines = outtemp.readlines()
        print lines
    except Exception, e:
        print traceback.format_exc()
    finally:
        if outtemp:
            outtemp.close()
    desc72_generate(nowtime + ".mp4")
    fingerprint_query(detailurl, nowtime + ".mp4" + ".desc72", headers)

if __name__ == "__main__":
    nowtime = str(datetime.datetime.now().microsecond)
    print nowtime
    detailurl = "https://zy.zxziyuan-yun.com/20180107/hv8I41wD/index.m3u8"
    t = threading.Thread(target=thread_download, args=(detailurl, url, nowtime))
    t.start()
    pass