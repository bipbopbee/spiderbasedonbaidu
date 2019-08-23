# coding:utf-8
from flask import Response, jsonify, render_template, abort, session, redirect, request, url_for, flash, send_file
# from flask import Blueprint, request,render_template, jsonify
# profile_home = Blueprint("profile", __name__)
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
from . import searches_home
@searches_home.route("/getall", methods=['POST','GET'])
def getall():
    print "getall"
    cursor.execute("select * from searches")
    collections = cursor.fetchall()
    print collections
    t = {}
    t['code'] = 0
    t['data'] = collections
    return json.dumps(t, ensure_ascii=False)

@searches_home.route("/getbyid", methods=['POST', 'GET'])
def getbyid():
    id = request.form.get('id')
    print id
    cursor.execute("select * from searches where id = " + id)
    collections = cursor.fetchone()
    print collections
    t = {}
    t['code'] = 0
    t['data'] = collections
    print t
    return json.dumps(t, ensure_ascii=False)

@searches_home.route("/searchbykeyword", methods=['POST', 'GET'])
def searchbykeyword():
    keyword = ""
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        print keyword
        t = threading.Thread(target = start_search, args=(keyword,))
        t.start()
    sql = "select * from searchengine where keyword = \'" + keyword + "\';"
    cursor.execute(sql)
    collections = cursor.fetchall()

    t = {}
    t['code'] = 0;
    t['data'] = collections
    
    return json.dumps(t, ensure_ascii=False)