# coding:utf-8
from flask import Response, jsonify, render_template, abort, session, redirect, request, url_for, flash, send_file
# from flask import Blueprint, request,render_template, jsonify
# profile_home = Blueprint("profile", __name__)
from . import profile_home
import os
from werkzeug.utils import secure_filename
import sys
sys.path.append("../..")
from videntify.curl2python import *
from searchengines.searchengine import *
from database.config import *
import threading
import json
import time
import pymysql
# conn = pymysql.connect(
#     host = '127.0.0.1',user = 'root',passwd = '123456',
#     port = 3306,db = 'videoright',charset = 'utf8'
#     #port必须写int类型
#     #charset必须写utf8，不能写utf-8
# )
conn = pool.connection()
cursor = conn.cursor()

content_id = ""
gerror = {"message":"success"}
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'mp4', 'desc72'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@profile_home.route('/file/upload', methods=['POST'])
def upload_part():  # 接收前端上传的一个分片
    task = request.form.get('task_id')  # 获取文件的唯一标识符
    chunk = request.form.get('chunk', 0)  # 获取该分片在所有分片中的序号
    filename = '%s%s' % (task, chunk)  # 构造该分片的唯一标识符

    upload_file = request.files['file']
    upload_file.save('./upload/%s' % filename)  # 保存分片到本地
    return render_template('upload.html')
@profile_home.route('/file/merge', methods=['GET'])
def upload_success():  # 按序读出分片内容，并写入新文件
    target_filename = request.args.get('filename')  # 获取上传文件的文件名
    task = request.args.get('task_id')  # 获取文件的唯一标识符
    videoname = request.args.get('videoname')
    chunk = 0  # 分片序号
    with open('./upload/%s' % target_filename, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError as msg:
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间

    absfilename = os.path.abspath('./upload/%s' % target_filename)
    print(absfilename)
    #desc72_generate(absfilename)
    apitoken = session['apitoken'].encode('raw_unicode_escape')
    headers = {"Authorization":apitoken}
    print (headers)
        # res = insertlocalfile(upload_path, headers)
        # result = json.loads(res.text)

        # if not result['error'] is None:
        #     error = result['error']['message']
        # else:
        #    content_id = result['data']['content']['contend_id']
    
    jobidstr = asyncinsertlocalfile(absfilename, headers)
    jobid = json.loads(jobidstr)['data']['job']['id']
    email = session['email']
    t = threading.Thread(target = threading_jobinsert, args=(videoname, headers, jobid,email, apitoken))
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    t.start()
    t.join()
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print ("upload" + content_id)
    return content_id + videoname
    #return render_template('profile/upload_ok.html')
    return send_file('static/profiles.html')
    return render_template('upload_ok.html', userinput=videoname, contentid = content_id, error = gerror['message'], val1=time.time())
    #return render_template('index.html')
@profile_home.route("/", methods=['POST', 'GET'])
def index():
    return "index"

@profile_home.route("/deletebyid", methods=['POST', 'GET'])
def deletebyid():
    id = ''
    if request.method == 'POST':
       id = request.form.get('id')
       print id
    sql = "delete from right_tmp where contentid = " + id
    cursor.execute(sql)
    conn.commit()

    sql = "delete from searches where contentid = " + id
    cursor.execute(sql)
    conn.commit()

    apitoken = session['apitoken'].encode('raw_unicode_escape')
    headers = {"Authorization":apitoken}
    deletecontent(id, headers)

    t = {}
    t['code'] = 0
    t['data'] = "done"

    return json.dumps(t,ensure_ascii=False)

@profile_home.route("/getall", methods=['POST', 'GET'])
def getall():
    cursor.execute("select *  from right_tmp where email = \'" + session['email'] + "\'")
    collections = cursor.fetchall()
    print collections
    t = {}
    t['code'] = 0
    #t['data'] = collections
    tmplist = []
    for i in range(len(collections)):
        tmp = {}
        tmp['rightid'] = collections[i][0]
        tmp['createtime'] = collections[i][1]
        tmp['rightname'] = collections[i][2]
        tmp['url'] = collections[i][3]
        tmp['email'] = collections[i][4]
        tmp['contentid'] = collections[i][5]
        tmplist.append(tmp)
    t['data'] = tmplist
    return json.dumps(t,ensure_ascii=False)

@profile_home.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        # f = request.files['file']
 
        # if not (f and allowed_file(f.filename)):
        #     return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
        # user_input = request.form.get("name")
        # #content_id = ''
        # error = ''
        # basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        # upload_path = os.path.join(basepath, 'static/videos', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # f.save(upload_path)
        
        # apitoken = session['apitoken'].encode('raw_unicode_escape')
        # headers = {"Authorization":apitoken}
        # print headers
        # # res = insertlocalfile(upload_path, headers)
        # # result = json.loads(res.text)

        # # if not result['error'] is None:
        # #     error = result['error']['message']
        # # else:
        # #    content_id = result['data']['content']['contend_id']
        # global content_id
        # global gerror
        # jobidstr = asyncinsertlocalfile(upload_path, headers)
        # jobid = json.loads(jobidstr)['data']['job']['id']
        # t = threading.Thread(target = threading_jobinsert, args=(user_input, headers, jobid))
        # t.start()
        # t.join()
        # print "upload" + content_id
        return send_file('static/profiles.html')
        #return render_template('profile/upload_ok.html')
        # return render_template('profile/upload_ok.html', userinput=user_input, contentid = content_id, error = gerror['message'], val1=time.time())
 
    return render_template('upload.html')

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
            print "thread" + content_id
            timestr = time.strftime('%Y-%m-%d %H:%M:%S')
            sql = "insert into right_tmp (rightid, createtime, rightname, url, email, contentid) values (NULL, \'"
            sql = sql + timestr + "\',\'" + rightname + "\'," + "'',\'" + email + "\'," + contentid + ")"
            print sql
            cursor.execute(sql)
            conn.commit()

            sql = "insert into searches (id, name, type, year, keyword, searchnums, lastsearchtime, contentid, apitoken) values (NULL, \'"
            sql = sql + rightname + "\', 'film', '2018', \'" + rightname + "\', \'0\', \'" + timestr + "\'," + contentid +",\'" + apitoken + "\')"
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