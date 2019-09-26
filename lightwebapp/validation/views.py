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
from . import validation_home

@validation_home.route("/getall",methods=['POST', 'GET'])
def getall():
    
    sql = "select * from privacy"
    cursor.execute(sql)
    collections = cursor.fetchall()

    print collections

    t = {}
    t['code'] = 0
    #t['data'] = collections
    tmplist = []
    for i in range(len(collections)):
        tmp = {}
        tmp['privacyid'] = collections[i][0]
        tmp['url'] = collections[i][1]
        tmp['rightname'] = collections[i][2]
        tmp['contentid'] = collections[i][3]
        tmp['hosturl'] = collections[i][4]
        tmplist.append(tmp)
    t['data'] = tmplist
    return json.dumps(t, ensure_ascii=False)

@validation_home.route("/getbyid", methods=['POST', 'GET'])
def getbyid():
    
    id = request.form.get('id')
    print id
    cursor.execute("select * from privacy where privacyid = " + id)
    collections = cursor.fetchone()

    print collections

    t = {}
    t['code'] = 0
    t['data'] = collections
    print t
    return json.dumps(t, ensure_ascii=False)