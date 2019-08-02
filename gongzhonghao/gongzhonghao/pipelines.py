# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

conn = pymysql.connect(
    host = '127.0.0.1',user = 'root',passwd = '123456',
    port = 3306,db = 'videoright',charset = 'utf8'
    #port必须写int类型
    #charset必须写utf8，不能写utf-8
)
cursor = conn.cursor()

class GongzhonghaoPipeline(object):
    def process_item(self, item, spider):
        url = item['url']
        title = item['title']
        publishname = item['publishname']
        publishdate = item['publishdate']
        sql = "insert into gongzhonghao (url, title, publishname, publishdate) values ("
        sql = sql + "\'" + url + "\' ,\'" + title + "\'  ,\'" + publishname + "\', \'" + publishdate + "\')"
        print sql
        cursor.execute(sql)
        conn.commit()
        return item
