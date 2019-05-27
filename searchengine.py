#coding=utf-8
import urllib
import urllib2
import re
import time
#解决utf8 code问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup

def getsearchpagebykeyword(url, keyword):
    wd = {'wd':keyword}
    wd = urllib.urlencode(wd)
    fullurl = url + wd
    return geturlpage(fullurl)
def geturlpage(url):
    data = ''
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    request = urllib2.Request(url = url, headers = headers)
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, err:
        print url + bytes(err.code)
    except urllib2.URLError, err:
        print err
        print url
    else:
        data = response.read()
    return data

#@return 返回视频网址list和下一页网址
def resolvepagedata(data):
    list = []
    retnexturl = ''
    soup = BeautifulSoup(data, 'lxml')
    nexturl = soup.find(name='a', text='下一页>')
    if nexturl:
        retnexturl = nexturl.get('href')
    for link in soup.find_all(name='a', attrs={'href':re.compile(r'^http:')}):
        list.append(link.get('href'))
    return (list, retnexturl)

#@return 返回码流地址
#测试地址1.https://www.haokongbu.com/play/471931.html
def getvideoadress(url):
    data = geturlpage(url)
    urlfilter = r'(?:https|http)://.+?\.(?:mp4|m3u8|mkv)'
    pattern = re.compile(urlfilter)
    return pattern.findall(data)
def main():
    #getvideoadress('https://www.haokongbu.com/play/471931.html')
    url = "http://www.baidu.com/s?"
    keyword = '美国队长1 在线观看'
    searchcount = 50
    n = 0
    data = getsearchpagebykeyword(url, keyword)
    while n < searchcount:
        websiteslist, nexturl = resolvepagedata(data)
        for website in websiteslist:
            #print website
            time.sleep(1)
            print getvideoadress(website)
        data = geturlpage(url+nexturl)  
        n = n + 1
    
    # data = getsearchpagebykeyword(url, keyword)
    # #print data
    # videolist = []
    # videolist, nexturl = resolvepagedata(data)
    # print videolist

if __name__ == '__main__':
    main()


    
    