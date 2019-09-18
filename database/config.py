#coding=utf-8
import pymysql
from DBUtils.PooledDB import PooledDB
# host = '127.0.0.1',user = 'root',passwd = '123456',
#     port = 3306,db = 'videoright',charset = 'utf8'
pool = PooledDB(pymysql, 10, host = '127.0.0.1',user = 'root',passwd = '123456',
    port = 3306,db = 'videoright',charset = 'utf8' )
conn = pool.connection()
# conn = pymysql.connect(
#     host = '127.0.0.1',user = 'root',passwd = '123456',
#     port = 3306,db = 'videoright',charset = 'utf8'
#     #port必须写int类型
#     #charset必须写utf8，不能写utf-8
# )