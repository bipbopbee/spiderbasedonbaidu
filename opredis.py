import redis
def lpush(key, value):
    r.lpush(key, value)
def rpush(key, value):
    r.rpush(key, value)
def lpop(key):
    return r.lpop(key)
def rpop(key):
    return r.rpop(key)
pool = redis.ConnectionPool(host = '127.0.0.1')
r = redis.Redis(connection_pool = pool)

if __name__ == '__main__':
    lpush('list', '1')
    lpush('list', '2')
    lpush('list', '3')

    print rpop('list')
    print rpop('list')
    print rpop('list')
