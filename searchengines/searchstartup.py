#coding=utf-8
from searchengines.aiqiyi import start_search as aiqiyi_search
from searchengines.bilibili import start_search as bilibili_search
from searchengines.meipai import start_search as meipai_search
from searchengines.youku import start_search as youku_search
from searchengines.tengxun import start_search as tengxun_search
import threading

def startsupall(keyword, apitoken):
    t = threading.Thread(target=aiqiyi_search, args=(keyword, apitoken))
    t.start()
    t = threading.Thread(target=bilibili_search, args=(keyword, apitoken))
    t.start()
    t = threading.Thread(target=meipai_search, args=(keyword, apitoken))
    t.start()
    t = threading.Thread(target=youku_search, args=(keyword, apitoken))
    t.start()
    t = threading.Thread(target=tengxun_search, args=(keyword, apitoken))
    t.start()
    pass

if __name__ == '__main__':
    print 'dd'
    #startsupall('钢铁侠'.encode('gbk'))