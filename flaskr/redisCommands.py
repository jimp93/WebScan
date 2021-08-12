import redis

r = redis.StrictRedis(host='localhost', port=6379, charset="utf-8", decode_responses=True)

rw = {'a':'fucksticks', 'b':'fanny'}

dog = 'cat'
r.hset(dog, 'a', 'tits')
r.hset(dog, 'b', 'fuck')
print(r.hget('cat', 'a'))
print(r.hmget('cat', 'a', 'b'))
print(r.hgetall('cat'))
r.hdel(dog, 'a')
print(r.hgetall('cat'))
r.delete('cat')
print(r.hgetall('cat'))

