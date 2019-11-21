#coding=utf-8
from dbHelper import *
class searchenginedbHelper(mySqlHelper):
    table = 'searchengine'
    def selectOne(self, prames):
        sql = "select * from searchengine where keyword = %s and name = %s and apitoken = %s"
        data = mySqlHelper.selectOne(self, sql, prames)
        return data

    def insert(self, prames):
        #"insert into searchengine (id, name, keyword, searchnums, searchtime)  values (NULL, '美拍', \'" + keyword.decode('gbk') +"\','0\',\'" + timestr + "\');"
        sql = "insert ignore into searchengine (id, name, keyword, searchnums, searchtime, apitoken)  values (%s, %s, %s, %s, %s, %s)"
        mySqlHelper.insert(self, sql, prames)
        pass

    def updateSearchtime(self, prames):
        #"update searchengine set searchtime=\'" + timestr + "\' where keyword=\'" + keyword.decode('gbk') + "\' and name = \'" + "美拍\';"
        sql = "update searchengine set searchtime=%s where keyword=%s and name = %s and apitoken = %s"
        mySqlHelper.update(self, sql, prames)
        pass

    def updateSearchnums(self, prames):
        sql = "update searchengine set searchnums=%s where keyword=%s and name = %s and apitoken = %s"
        mySqlHelper.update(self, sql, prames)
        pass

if __name__ == "__main__":
    dbhelper = searchenginedbHelper()
    print dbhelper.selectOne(('美国队长','谷歌'))
    pass