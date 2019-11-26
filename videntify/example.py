#coding=utf-8
import urllib
import urllib2
import requests
import os
from requests.auth import  HTTPBasicAuth
import sys
sys.path.append("..")
from curl2python import *
from download import *
import platform
import subprocess
import tempfile
import traceback
import re
import threading
lock = threading.Lock()
singlelen = 5
def thread_download1(url):
    command = "ffmpeg -i " + url
    sysstr = platform.system()
    try:
        outtemp =tempfile.SpooledTemporaryFile(bufsize = 100 * 1000)
        fileno = outtemp.fileno()
        if sysstr == 'Windows':
            fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=False)
        else:
            fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=True)
        fd.communicate()
        outtemp.seek(0)
        lines = outtemp.readlines()
        print lines
        filter = re.compile('Duration: (.*?),')
        referer = filter.findall(str(lines))[0]
        print referer
        totallen =  getTimelen(referer)
        index = int(totallen) / (singlelen*60)  
        last = totallen % (singlelen*60)
        i = 0
        print totallen
        print index
        print last
        for i in range(index):
            start = i *singlelen*60
            m,s = divmod(start, 60)
            h,m = divmod(m, 60)
            startstr = str(h) + ":" + str(m) + ":" + str(s)
            t = threading.Thread(target=thread_split, args=(url, startstr, singlelen*60, i))
            t.start()
        m,s = divmod(i*singlelen*60, 60)
        h,m = divmod(m, 60)
        startstr = str(h) + ":" + str(m) + ":" + str(s)
        t = threading.Thread(target=thread_split, args=(url, startstr, last, i+1))
        t.start()
    except Exception, e:
        print traceback.format_exc()
    finally:
        if outtemp:
            outtemp.close()
def getTimelen(timelen):
    min = 0
    strs = timelen.split(":")
    if (int(strs[0]) > 0):
        min = int(strs[0]) * 60 * 60
    if (int(strs[1]) > 0):
         min = min + int(strs[1]) * 60
    if (float(strs[2]) > 0):
        min =min + float(strs[2])
    return min
def video_split(url, start, duration, index):
    filename = str(index) + ".mp4"
    command = "ffmpeg -ss " + str(start) + " -t " + str(duration) + " -accurate_seek -i " + url + " -codec copy -avoid_negative_ts 1 " + filename
    print command
    sysstr = platform.system()
    fd = 0
    try:
        outtemp =tempfile.SpooledTemporaryFile(bufsize = 100 * 1000)
        fileno = outtemp.fileno()
        if sysstr == 'Windows':
            fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=False)
        else:
            fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=True)
        fd.communicate()
        outtemp.seek(0)
        lines = outtemp.readlines()
        #print lines
    except Exception, e:
        print traceback.format_exc()
    finally:
        if outtemp:
            outtemp.close()
    #return
    while fd.poll() is None:
        pass
def thread_split(url, start, duration, index):
    t = threading.Thread(target=video_split, args=(url, start, singlelen*60, index))
    t.start()
    t.join()
    #ffmpeg -ss 1:10:30 -t 120 -accurate_seek -i test.mp4 -codec copy -avoid_negative_ts 1 out.mp4
    filename = str(index) + ".mp4"
    # command = "ffmpeg -ss " + str(start) + " -t " + str(duration) + " -accurate_seek -i " + url + " -codec copy -avoid_negative_ts 1 " + filename
    # print command
    # sysstr = platform.system()
    # fd = 0
    # try:
    #     outtemp =tempfile.SpooledTemporaryFile(bufsize = 100 * 1000)
    #     fileno = outtemp.fileno()
    #     if sysstr == 'Windows':
    #         fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=False)
    #     else:
    #         fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=True)
    #     fd.communicate()
    #     outtemp.seek(0)
    #     lines = outtemp.readlines()
    #     print lines
    # except Exception, e:
    #     print traceback.format_exc()
    # finally:
    #     if outtemp:
    #         outtemp.close()
    # #return
    # while fd.poll() is None:
    #     pass
    #desc72_generate(filename)
    t = threading.Thread(target=desc72_generate, args=(filename,))
    t.start()
    t.join()
    #return
    os.remove(filename)
    headers = {"Authorization":"LWtrKgMmLIeAWyyDUlLa"}
    jobidstr = asyncinsertlocalfile(filename + ".desc72", headers)
    print jobidstr
    jobid = json.loads(jobidstr)['data']['job']['id']
    #email = session['email']
    email = "5168@qq.com"
    apitoken = "LWtrKgMmLIeAWyyDUlLa"
    videoname = "u571"
    t = threading.Thread(target = threading_jobinsert, args=(videoname, headers, jobid,email, apitoken))
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    t.start()
    t.join()
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
def threading_jobinsert(rightname, headers, jobid, email, apitoken):
    global content_id
    while True:
        statusstr = queryjobstatus(jobid, headers = headers)
        print statusstr + jobid
        status = json.loads(statusstr)['data']['job']['status']
        contentid = ''
        time.sleep(1)
        if status == 'success':
            link = json.loads(statusstr)['data']['job']['result_url']
            datastr = querypersistedresult(link, headers)
            print datastr
            contentid = json.loads(datastr)['data']['content']['content_id']
            content_id = contentid
            deletecontent(contentid, {"Authorization":"LWtrKgMmLIeAWyyDUlLa"})
            print "thread" + content_id
            timestr = time.strftime('%Y-%m-%d %H:%M:%S')
            sql = "select * from right_tmp where rightname = \'" + rightname + "\' and email = \'" + email + "\'"
            cursor.execute(sql)
            collections = cursor.fetchall()
            print collections
            if len(collections) == 0:
                sql = "insert into right_tmp (rightid, createtime, rightname, url, email, contentid) values (NULL, \'"
                sql = sql + timestr + "\',\'" + rightname + "\'," + "'',\'" + email + "\',\':" + contentid + ":\')"
                print sql
                cursor.execute(sql)
                conn.commit()
            else:
                lastcontentid = collections[0][5] + contentid + ":"
                sql = "update right_tmp set contentid = \'" + lastcontentid + "\' where rightname = \'" + rightname + "\' and email = \'" + email + "\'"  
                print sql
                lock.acquire()
                cursor.execute(sql)
                conn.commit()
                lock.release()
            sql = "select * from searches where keyword = \'" + rightname + "\' and apitoken = \'" + apitoken + "\'"
            cursor.execute(sql)
            collections = cursor.fetchall()
            print collections
            if len(collections) == 0:
                sql = "insert into searches (id, name, type, year, keyword, searchnums, lastsearchtime, contentid, apitoken) values (NULL, \'"
                sql = sql + rightname + "\', 'film', '2018', \'" + rightname + "\', \'0\', \'" + timestr + "\',\':" + contentid +":\',\'" + apitoken + "\')"
                print sql
                cursor.execute(sql)
                conn.commit()
            else:
                lastcontentid = collections[0][7] + contentid + ":"
                sql = "update searches set contentid = \'" + lastcontentid + "\' where keyword = \'" + rightname + "\' and apitoken = \'" + apitoken + "\'"  
                print sql
                lock.acquire()
                cursor.execute(sql)
                conn.commit()
                lock.release()
            break
        elif status == 'error':
            global gerror
            gerror = json.loads(statusstr)['data']['job']['error']
            break
        elif status == 'cancelled':
            break
    pass
if __name__ == '__main__':
    #  headers = {"Authorization":"LWtrKgMmLIeAWyyDUlLa"}
    #  payload = {'download_url': 'http://127.0.0.1:5000/static/images/2.MP4'}
    #  res = requests.post(BASE_URL + ACTION_QUERY_ASYNC, headers = headers, data = payload)
    #  print res.text
    #  print asyncqueryurl('http://127.0.0.1:5000/static/images/2.MP4', headers)
    #  post_byrequest()
    #  delete_byrequest()
    #  put_byrequest()
    #  post_byurllib2()
    # process = CrawlerProcess()
    # process.crawl(VideoobserverSpider)
    # process.start()
    #curl -X DELETE -H "Authorization: LWtrKgMmLIeAWyyDUlLa" http://39.97.252.185/api/v1/contents/240247
    #curl -H "Authorization: LWtrKgMmLIeAWyyDUlLa" http://39.97.252.185/api/v1/contents
    thread_download1("test.mp4")

    pass
    

