#coding=utf-8
import requests
import os
import time
#BASE_URL = "http://39.97.164.155/api/v1"
BASE_URL = "http://39.97.252.185/api/v1"
"""
用户操作定义
"""
ACTION_CONTENT = "/contents"
ACTION_INSERT = "/insert"
ACTION_INSERT_ASYNC = "/insert_async"
ACTION_QUERY = "/query"
ACTION_QUERY_ASYNC = "/query_async"
ACTION_QUERY_WITHIN = "/query_sw"
ACTION_QUERY_WITHIN_ASYNC = "/query_sw_async"
ACTION_JOBS = "/jobs"
ACTION_QUERY_PERSISTED_RESULT = "/query_results"
ACTION_QUERY_WITHIN_PERSISTED_RESULT = "/query_results_sw"
ACTION_UPDATE_METADATA = "/contents"
ACTION_GET_DB_INFO = "/dbinfo"
"""
 添加删除用户
"""
ACTION_USERS_CREATE  = "/users"
ACTION_USERS_DELETE = "/users"
ACTION_USERS_LIST = "/users"
ACTION_USER_ACCOUNT = "/account"
ACTION_USER_INFOMATION = "/users"
"""
插入文件
"""
"""
参数：
返回值：{
    "data": {
        "content": {
            "content_id": "240257",
            "duration": null,
            "metadata": {},
            "url": "https://sve.videntifier.com/data/a23aeb17ed6c31771a072cf628a42fc4d56e8106.png",
            "sha1sum": "a23aeb17ed6c31771a072cf628a42fc4d56e8106",
            "type": "image",
            "filename": "1.jpg.png",
            "file_size": "558087",
            "scaled_height": "303",
            "scaled_width": "539",
            "nr_points": "471",
            "created_at": "2019-06-27T16:04:56.473786+08:00",
            "username": "sushuai",
            "insert_method": "content"
        }
    }
}
"""
def insertlocalfile(filepath, headers):
    if os.path.isfile(filepath):
        file = open(filepath, 'rb')
        payload = {"file": file}
        print payload
        print headers
        print BASE_URL + ACTION_INSERT
        res = requests.post(BASE_URL + ACTION_INSERT, headers = headers, files = payload)
        return res.text
def asyncinsertlocalfile(filepath, headers):
    if os.path.isfile(filepath):
        file = open(filepath, 'rb')
        payload = {'file': file}
        res = requests.post(BASE_URL + ACTION_INSERT_ASYNC, headers = headers, files = payload)
        return res.text
def inserturl(url, headers):
    payload = {'download_url': url}
    res = requests.post(BASE_URL + ACTION_INSERT, headers = headers, files = payload)
    return res.text
def asyncinserturl(url, headers):
    payload = {'download_url': url}
    res = requests.post(BASE_URL + ACTION_INSERT_ASYNC, headers = headers, files = payload)
    return res.text
"""
查询匹配
返回值：
 {
   "data": {
        "query": {
            "id": "4",
            "type": "image",
            "file": "2.jpg.png"
        },
        "matches": [
            {
                "content": {
                    "content_id": "240252",
                    "duration": null,
                    "metadata": {},
                    "url": "https://sve.videntifier.com/data/a23aeb17ed6c31771a072cf628a42fc4d56e8106.png",
                    "sha1sum": "a23aeb17ed6c31771a072cf628a42fc4d56e8106",
                    "type": "image",
                    "filename": "1.jpg.png",
                    "file_size": "558087",
                    "scaled_height": "303",
                    "scaled_width": "539",
                    "nr_points": "471",
                    "created_at": "2019-06-27T10:45:31.364572+08:00",
                    "username": "sve",
                    "insert_method": "content"
                },
                "nr_matching_points": "33",
                "coverage": null,
                "match_type": "similarity"
            },
            {
                "content": {
                    "content_id": "240257",
                    "duration": null,
                    "metadata": {},
                    "url": "https://sve.videntifier.com/data/a23aeb17ed6c31771a072cf628a42fc4d56e8106.png",
                    "sha1sum": "a23aeb17ed6c31771a072cf628a42fc4d56e8106",
                    "type": "image",
                    "filename": "1.jpg.png",
                    "file_size": "558087",
                    "scaled_height": "303",
                    "scaled_width": "539",
                    "nr_points": "471",
                    "created_at": "2019-06-27T16:04:56.473786+08:00",
                    "username": "sushuai",
                    "insert_method": "content"
                },
                "nr_matching_points": "33",
                "coverage": null,
                "match_type": "similarity"
            }
        ],
        "_metadata": {
            "page": "1",
            "page_size": "50",
            "nr_pages": "1",
            "nr_results": "2",
            "links": {
                "self": "https://sve.videntifier.com/api/v1/query_results/4?access_token=dje0TMHQ06aSPUJVbsJjPATz7PaXQdf4&page=1&page_size=50",
                "next": null,
                "prev": null,
                "first": "https://sve.videntifier.com/api/v1/query_results/4?access_token=dje0TMHQ06aSPUJVbsJjPATz7PaXQdf4&page=1&page_size=50",
                "last": "https://sve.videntifier.com/api/v1/query_results/4?access_token=dje0TMHQ06aSPUJVbsJjPATz7PaXQdf4&page=1&page_size=50"
            }
        }
    }
}
"""
def querylocalfile(filepath, headers):
    if os.path.isfile(filepath):
        file = open(filepath, 'rb')
        payload = {'file': file}
        res = requests.post(BASE_URL + ACTION_QUERY, headers = headers, files = payload)
        return res.text
def asyncquerylocalfile(filepath, headers):
    if os.path.isfile(filepath):
        file = open(filepath, 'rb')
        payload = {'file': file}
        res = requests.post(BASE_URL + ACTION_QUERY_ASYNC, headers = headers, files = payload)
        return res.text
def queryurl(url, headers):
    payload = {'download_url': url}
    res = requests.post(BASE_URL + ACTION_QUERY, headers = headers, data = payload)
    return res.text
def asyncqueryurl(url, headers):
    payload = {'download_url': url}
    res = requests.post(BASE_URL + ACTION_QUERY_ASYNC, headers = headers, data = payload)
    return res.text
def querycontentid(content_id, headers):
    payload = {'content_id': content_id}
    res = requests.post(BASE_URL + ACTION_QUERY, headers = headers, data = payload)
    return res.text
def aysncquerycontentid(content_id, headers):
    payload = {'content_id': content_id}
    res = requests.post(BASE_URL + ACTION_QUERY_ASYNC, headers = headers, data = payload)
    return res.text
"""
使用within mode查询，只对视频有效

"""
def queywithinfile(filepath, headers):
    if os.path.isfile(filepath):
        file = open(filepath, 'rb')
        payload = {'file': file}
        res = requests.post(BASE_URL + ACTION_QUERY_WITHIN, headers = headers, files = payload)
        return res.text
def asyncquerywithfile(filepath ,headers):
    if os.path.isfile(filepath):
        file = open(filepath, 'rb')
        payload = {'file': file}
        res = requests.post(BASE_URL + ACTION_QUERY_WITHIN_ASYNC, headers = headers, files = payload)
        return res.text
"""
async insert/query时，服务器后台生成的jobs操作
"""
def queryjobstatus(jobid, headers):
    res = requests.get(BASE_URL + ACTION_JOBS + "/" + jobid, headers = headers, allow_redirects=False)
    return res.text
"""
查询已经查询过的结果
以前查询过的结果
"_metadata": {
            "page": "1",
            "page_size": "50",
            "nr_pages": "1",
            "nr_results": "2",
            "links": {
                "self": "https://sve.videntifier.com/api/v1/query_results/5?access_token=6CChvv3IHhfi6Q8IL1Y6QRNvytayHbF6&page=1&page_size=50",
                "next": null,
                "prev": null,
                "first": "https://sve.videntifier.com/api/v1/query_results/5?access_token=6CChvv3IHhfi6Q8IL1Y6QRNvytayHbF6&page=1&page_size=50",
                "last": "https://sve.videntifier.com/api/v1/query_results/5?access_token=6CChvv3IHhfi6Q8IL1Y6QRNvytayHbF6&page=1&page_size=50"
            }
"""
##link = /5?access_token=6CChvv3IHhfi6Q8IL1Y6QRNvytayHbF6
def querypersistedresult(link, headers):
    res = requests.get(link, headers = headers)
    return res.text
def querywithinpersistedresult(link ,headers):
    res = requests.post(BASE_URL + ACTION_QUERY_WITHIN_PERSISTED_RESULT + link, headers = headers)
    return res.text

def useraccount(headers):
    res = requests.post(BASE_URL + ACTION_USER_ACCOUNT, headers = headers)
    return res.text
def userinfomation(id, headers):
    res = requests.post(BASE_URL + ACTION_USER_INFOMATION + "/" + id, headers = headers)
    return res.text
def userlist(headers):
    res = requests.post(BASE_URL + ACTION_USERS_LIST, headers = headers)
    return res.text
def usercreate(email, name, headers):
    files = {"email":email, "username":name}
    res = requests.post(BASE_URL + ACTION_USERS_CREATE, headers = headers, files = files)
    return res.text
def userdelete(id, headers):
    res = requests.post(BASE_URL + ACTION_USERS_DELETE + "/" + id, headers = headers)
    return res.text
def updatemetadata(content_id, headers):
    res = requests.delete(BASE_URL + ACTION_UPDATE_METADATA + "/" + content_id + "/metadata", headers = headers)
    return res.text
def getcontentinfo(content_id, headers):
    res = requests.post(BASE_URL + ACTION_CONTENT + "/" + content_id, headers = headers)
    return res.text
def listcontents(headers):
    res = requests.post(BASE_URL + ACTION_CONTENT, headers = headers)
    return res.text
def deletecontent(content_id, headers):
    res = requests.delete(BASE_URL + ACTION_CONTENT + "/" + content_id, headers = headers)
    return res.text
def getdbinfo(headers):
    print BASE_URL + ACTION_GET_DB_INFO
    res = requests.post(BASE_URL + ACTION_GET_DB_INFO, headers = headers)
    return res.text

    
