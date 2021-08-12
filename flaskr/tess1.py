import nltk
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import newspaper
from newspaper import news_pool
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from newspaper import Article, Source
sns.set_context("talk")
sns.set_style("whitegrid")
import seaborn as sns
import string
import os

stop_words_s = open('C:/Users/james/PycharmProjects/WebScan/stop_words_english.txt', encoding='utf-8').read()
stop_words_l = (stop_words_s.split())
stop_words_l.sort()

stop_words = set(stop_words_l)


bbc = newspaper.build('http://bbc.co.uk', memoize_articles=False)
gd = newspaper.build('http://guardian.co.uk', memoize_articles=False)
cnn = newspaper.build('http://cnn.com', memoize_articles=False)
mail = newspaper.build('https://www.dailymail.co.uk', memoize_articles=False)

words_raw = []
papers = [bbc, gd, cnn, mail]
news_pool.set(papers, threads_per_source=2)
news_pool.join()

words_string = ''
wordcloud_l = []
freq = {}
NUM_KEYWORDS = 10
for article in mail.articles:
    words_string = ''
    article.parse()
    words_string += article.text
    words_list = words_string.split()
    if words_list:
        num_words = len(words_list)
        for word in words_list:
            word = word.translate(str.maketrans("", "", string.punctuation))
            word = word.lower()
            if word:
                if word not in stop_words_l:
                    wordcloud_l.append(word)
                    if word in freq:
                        freq[word] += 1
                    else:
                        freq[word] = 1

wordcloud_s = ' '.join(wordcloud_l)

keywords = sorted(freq.items(),
                  key=lambda x: (x[1], x[0]),
                  reverse=True)
keywords = keywords[:25]
labels = list((i[0] for i in keywords))
frequencies = list((i[1] for i in keywords))

ticks = np.arange(len(keywords))


fig, ax = plt.subplots(figsize=(12, 10))
sns.set_context('poster')
sns.barplot(x=frequencies, y=labels)
ax.invert_yaxis()
plt.title('Guardian keywords')
plt.ylabel('Word')
plt.show()


wordcloud = WordCloud(stopwords=stop_words, background_color="white", width=800, height=400).generate(wordcloud_s)

fig1, ax1 = plt.subplots(figsize=(18, 10))
plt.imshow(wordcloud, interpolation='bicubic')
plt.axis("off")
plt.show()





# import time
# import dramatiq
# import redis
# from dramatiq.brokers.redis import RedisBroker
# from dramatiq.results.backends import RedisBackend
# from dramatiq.results import Results
# from dramatiq.middleware import CurrentMessage
#
#
# result_backend = RedisBackend(url="redis://127.0.0.1:6379")
# broker = RedisBroker(url="redis://127.0.0.1:6379")
# broker.add_middleware(Results(backend=result_backend))
# broker.add_middleware(CurrentMessage())
# dramatiq.set_broker(broker)
#
#
# r = redis.Redis(host='localhost', port=6379, charset="utf-8", decode_responses=True)
#
#
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
