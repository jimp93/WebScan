# import os
#
import redis
from waitress import serve
import time
r = redis.Redis(host='localhost', port=6379, charset="utf-8", decode_responses=True)

# from rq import Worker, Queue, Connection
#
# listen = ['default']
#
# redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
#
# conn = redis.from_url(redis_url)
#
# if __name__ == '__main__':
#     with Connection(conn):
#         worker = Worker(list(map(Queue, listen)))
#         worker.work()
#

import uuid

jid = uuid.uuid4()

print(jid)



