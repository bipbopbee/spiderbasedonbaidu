# coding:utf-8
from flask import Response, jsonify, render_template, abort, session, redirect, request, url_for, flash
# from flask import Blueprint, request,render_template, jsonify
# profile_home = Blueprint("profile", __name__)
from . import profile_home
import os
from werkzeug.utils import secure_filename
import sys
sys.path.append("../..")
from videntify.curl2python import *
from searchengines.searchengine import *
import threading
import json
import time
import pymysql
conn = pymysql.connect(
    host = '127.0.0.1',user = 'root',passwd = '123456',
    port = 3306,db = 'videoright',charset = 'utf8'
    #port必须写int类型
    #charset必须写utf8，不能写utf-8
)
cursor = conn.cursor()

content_id = ""
gerror = {"message":"success"}
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'mp4', 'desc72'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@profile_home.route("/", methods=['POST', 'GET'])
def index():
    return "index"

@profile_home.route("/getall", methods=['POST', 'GET'])
def getall():
    cursor.execute("select *  from right_tmp")
    collections = cursor.fetchall()
    print collections
    t = {}
    t['code'] = 0
    t['data'] = collections
    return json.dumps(t,ensure_ascii=False)

@profile_home.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
        user_input = request.form.get("name")
        #content_id = ''
        error = ''
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        upload_path = os.path.join(basepath, 'static/videos', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        
        apitoken = session['apitoken'].encode('raw_unicode_escape')
        headers = {"Authorization":apitoken}
        print headers
        # res = insertlocalfile(upload_path, headers)
        # result = json.loads(res.text)

        # if not result['error'] is None:
        #     error = result['error']['message']
        # else:
        #    content_id = result['data']['content']['contend_id']
        global content_id
        global gerror
        jobidstr = asyncinsertlocalfile(upload_path, headers)
        jobid = json.loads(jobidstr)['data']['job']['id']
        t = threading.Thread(target = threading_jobinsert, args=(user_input, headers, jobid))
        t.start()
        t.join()
        print "upload" + content_id
        return render_template('profile/upload_ok.html', userinput=user_input, contentid = content_id, error = gerror['message'], val1=time.time())
 
    return render_template('upload.html')

def threading_jobinsert(rightname, headers, jobid):
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
            print "thread" + content_id
            timestr = time.strftime('%Y-%m-%d %H:%M:%S')
            sql = "insert into right_tmp (rightid, createtime, rightname, url, email, contentid) values (NULL, \'"
            sql = sql + timestr + "\',\'" + rightname + "\'," + "'',\'" + "516854715@qq.com\'," + contentid + ")"
            print sql
            cursor.execute(sql)
            conn.commit()

            sql = "insert into searches (id, name, type, year, keyword, searchnums, lastsearchtime) values (NULL, \'"
            sql = sql + rightname + "\', 'film', '2018', \'" + rightname + "\', \'0\', \'" + timestr + "\')"
            print sql
            cursor.execute(sql)
            conn.commit()

            break
        elif status == 'error':
            global gerror
            gerror = json.loads(statusstr)['data']['job']['error']
            break
        elif status == 'cancelled':
            break
    pass