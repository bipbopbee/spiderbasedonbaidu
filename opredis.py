import redis
def lpush(key, value):
    r.rpush(key, value)
pool = redis.ConnectionPool(host = '127.0.0.1')
r = redis.Redis(connection_pool = pool)
lpush('myspider:start_urls', 'http://www.jiaoyizhe.com/forum-16-1.html')
lpush('myspider:start_urls', 'http://www.baidu.com')


