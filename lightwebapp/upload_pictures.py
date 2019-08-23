# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify,session
from werkzeug.utils import secure_filename
import os
import time
from datetime import timedelta
import json
import sys
sys.path.append("..")
from videntify.curl2python import *
from searchengines.searchengine import *
import threading
import pymysql
#from scrapy.crawler import CrawlerProcess
#from CopyrightObserver.CopyrightObserver.spiders.VideoObserver import VideoobserverSpider
conn = pymysql.connect(
    host = '127.0.0.1',user = 'root',passwd = '123456',
    port = 3306,db = 'videoright',charset = 'utf8'
    #port必须写int类型
    #charset必须写utf8，不能写utf-8
)
content_id = ""
gerror = {"message":"success"}
cursor = conn.cursor()
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'mp4', 'desc72'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
app.secret_key = '123456'

#注册blue_print
from profile.views import profile_home as profile_blueprint
app.register_blueprint(profile_blueprint, url_prefix="/profile")

from searches.views import searches_home as searches_blueprint
app.register_blueprint(searches_blueprint, url_prefix="/searches")

from validation.views import validation_home as validation_blueprint
app.register_blueprint(validation_blueprint, url_prefix="/validation")

@app.route('/index', methods=['POST', 'GET'])
def home():
    return render_template('login.html')
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get("user")
        password = request.form.get("passwd")
        print username
        print password
        cursor.execute("select *  from user where username = \'" + username + "\' and userpassword = \'" + password + "\'")
        row = cursor.fetchall()
        print row
        if len(row) == 0:
            return url_for("login")
        else:
            session.permanent = True
            session['username'] = username
            session['apitoken'] = row[0][4]
            return url_for("ui")
            #return url_for("upload")

@app.route('/ui', methods=['POST', 'GET'])
def ui():
    return render_template('test.html')
@app.route('/main', methods=['POST', 'GET'])
def main():
    return render_template('upload.html')
# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
        user_input = request.form.get("name")
        #content_id = ''
        error = ''
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
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
        return render_template('upload_ok.html', userinput=user_input, contentid = content_id, error = gerror['message'], val1=time.time())
 
    return render_template('upload.html')
 
@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        print keyword
        # start_search(keyword)
        # spider = VideoobserverSpider(session['apitoken'].encode('raw_unicode_escape'))
        # process = CrawlerProcess()
        # process.crawl(spider)
        # process.start()
        t = threading.Thread(target = start_search, args=(keyword,))
        t.start()
        return render_template('search.html')
    return render_template('search.html')
@app.route('/update', methods=['POST','GET'])
def update():
    cursor.execute("select *  from privacy")
    collections = cursor.fetchall()
    print collections
    t = {}
    t['data'] = collections
    return json.dumps(t,ensure_ascii=False)
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
            sql = "insert into right_tmp (rightid, rightname, url, email, contentid) values (NULL, \'"
            sql = sql + rightname + "\'," + "'',\'" + "516854715@qq.com\'," + contentid + ")"
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
if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=5000, debug=True)