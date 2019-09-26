# coding:utf-8
from flask import Response, jsonify, render_template, abort, session, redirect, request, url_for, flash, send_file
# from flask import Blueprint, request,render_template, jsonify
# profile_home = Blueprint("profile", __name__)
import os
from werkzeug.utils import secure_filename
import sys
sys.path.append("../..")
from videntify.curl2python import *
from searchengines.searchstartup import *
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
    cursor = conn.cursor()
    print "getall"
    cursor.execute("select * from searches")
    collections = cursor.fetchall()
    cursor.close()
    print collections
    t = {}
    t['code'] = 0
    #t['data'] = collections
    tmplist = []
    for i in range(len(collections)):
        tmp = {}
        tmp['id'] = collections[i][0]
        tmp['name'] = collections[i][1]
        tmp['type'] = collections[i][2]
        tmp['year'] = collections[i][3]
        tmp['keyword'] = collections[i][4]
        tmp['searchnums'] = collections[i][5]
        tmp['lastsearchtime'] = collections[i][6]
        tmplist.append(tmp)

    t['data'] = tmplist
    return json.dumps(t, ensure_ascii=False)

@searches_home.route("/getbyid", methods=['POST', 'GET'])
def getbyid():
    cursor = conn.cursor()
    id = request.form.get('id')
    print id
    cursor.execute("select * from searches where id = " + id)
    collections = cursor.fetchone()
    cursor.close()
    print collections
    t = {}
    t['code'] = 0
    t['data'] = collections
    print t
    return json.dumps(t, ensure_ascii=False)

@searches_home.route("/searchbykeyword", methods=['POST', 'GET'])
def searchbykeyword():
    cursor = conn.cursor()
    keyword = ""
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        print keyword
        t = threading.Thread(target = startsupall, args=(keyword.encode('gbk'),))
        t.start()

    sql = "select * from searches where keyword = \'" + keyword + "\';"
    cursor.execute(sql)
    cursor.close
    row = cursor.fetchone()
    id = row[0]
    num = int(row[5])
    num = num + 1
    sql = "update searches set searchnums=\'" + str(num) + "\' where id = " + str(id)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()

    cursor = conn.cursor()
    sql = "select * from searchengine where keyword = \'" + keyword + "\';"
    cursor.execute(sql)
    collections = cursor.fetchall()
    cursor.close()
    t = {}
    t['code'] = 0
    #t['data'] = collections
    tmplist = []
    for i in range(len(collections)):
        tmp = {}
        tmp['id'] = collections[i][0]
        tmp['name'] = collections[i][1]
        tmp['keyword'] = collections[i][2]
        tmp['searchnums'] = collections[i][3]
        tmp['lastsearchtime'] = collections[i][4]
        tmplist.append(tmp)
    t['data'] = tmplist

    return json.dumps(t, ensure_ascii=False)

@searches_home.route("/getsearchengine", methods=['POST', 'GET'])
def getsearchengine():
    cursor = conn.cursor()
    keyword = ''
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        print keyword
    sql = "select * from searchengine where keyword = \'" + keyword + "\';"
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()

    t = {}
    t['code'] = 0
    t['data'] = row

    return json.dumps(t, ensure_ascii=False)