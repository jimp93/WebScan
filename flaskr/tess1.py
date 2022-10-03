
import time
import dramatiq
import redis
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results.backends import RedisBackend
from dramatiq.results import Results
from dramatiq.middleware import CurrentMessage

result_backend = RedisBackend(url="redis://127.0.0.1:6379")
broker = RedisBroker(url="redis://127.0.0.1:6379")
broker.add_middleware(Results(backend=result_backend))
broker.add_middleware(CurrentMessage())
dramatiq.set_broker(broker)
#
#
r = redis.Redis(host='localhost', port=6379, charset="utf-8", decode_responses=True)

#
# @dramatiq.actor()
# def hello(x,y):
#     s = CurrentMessage.get_current_message().message_id
#     print(s)


# jvar = ''

#
# def q_job():
#     job = q.enqueue_call(
#         func=start_logic(), result_ttl=5000)
#     qq = job.get_id()
#     print(qq)
#     global jvar
#     jvar = qq
#     return jvar
#
#
# def get_results(job_key):
#     job = Job.fetch(job_key, connection=conn)
#     if job.is_finished:
#         print('Ya')
#     else:
#         print('Nah')
#
#
# def trigger(jvar):
#     time.sleep(4)
#     get_results(jvar)
#
#
# q_job()
# trigger(jvar)
#
