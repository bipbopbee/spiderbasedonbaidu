# coding:utf-8
from flask import Response, jsonify, render_template, abort, session, redirect, request, url_for, flash
# from flask import Blueprint, request,render_template, jsonify
# profile_home = Blueprint("profile", __name__)
from . import appium_home
import os
import sys
sys.path.append("../..")
from database.opredis import *
from database.config import *
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

@appium_home.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        table = request.form.get('table')
        keyword = request.form.get('keyword')
        title = request.form.get('title')
        detailurl = request.form.get('detailurl')
        videourl = request.form.get('videourl')
        upname = request.form.get('upname')

        value = {
           'table':table,
           'keyword':keyword,
           'title':title,
           'detailurl':detailurl,
           'videourl':videourl,
           'upname':upname 
        }
        #f = open('appresult.txt', 'w+')
        with open('appresult.txt', 'a+') as f:
            f.write(str(value) + '\n')
        lpush('list', json.dumps(value))

        t = {}
        t['code'] = 0
        t['data'] = "done"
        return json.dumps(t,ensure_ascii=False)
    else:    
        t = {}
        t['code'] = 0
        t['data'] = "error"
        return json.dumps(t,ensure_ascii=False)