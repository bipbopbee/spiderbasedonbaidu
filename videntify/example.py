#coding=utf-8
import urllib
import urllib2
import requests
import os
from requests.auth import  HTTPBasicAuth
from curl2python import *
header = {"Authorization" : "LWtrKgMmLIeAWyyDUlLa"}
url = "http://39.97.164.155/api/v1/"
action_contents = "contents"
action_insert = "insert"

files = open("D:\\videntify\\1.jpg.png",'rb')
def post_byrequest():
    headers = {"Authorization": "LWtrKgMmLIeAWyyDUlLa"}
    payload = {"file":files}
    res = requests.post(url + action_insert, headers = headers, files = payload)
    print  res.text
def delete_byrequest():
    headers = {"Authorization": "LWtrKgMmLIeAWyyDUlLa"}
    res = requests.delete(url + action_contents + "/240255", headers = headers)
    print  res.text
def put_byrequest():
    headers = {"Authorization": "LWtrKgMmLIeAWyyDUlLa"}
    payload = {"internal_id":"320349"}
    res = requests.put(url + action_contents + "/240254/metadata", headers = headers)
    print res.text
if __name__ == '__main__':
     headers = {"Authorization":"LWtrKgMmLIeAWyyDUlLa"}
     res = getdbinfo(headers = headers)
     print res.text
     res = requests.post(url + "/dbinfo", headers = headers)
     print res.text
    #post_byrequest()
    #delete_byrequest()
    #put_byrequest()
    #post_byurllib2()
    
