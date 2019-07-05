# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
from datetime import timedelta
from curl2python import *
import json
import sys
from searchengine import *
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'mp4'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
 
 
# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
        user_input = request.form.get("name")
        content_id = ''
        error = ''
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        
        headers = {"Authorization":"LWtrKgMmLIeAWyyDUlLa"}
        res = insertlocalfile(upload_path, headers)
        result = json.loads(res.text)
        if result['error']:
            error = result['error']['message']
        else:
           content_id = result['data']['content']['contend_id']
 
        return render_template('upload_ok.html',userinput=user_input,contentid = content_id, error = error, val1=time.time())
 
    return render_template('upload.html')
 
@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        print keyword
        start_search(keyword)
        pass
    return render_template('search.html')
if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=5000, debug=True)