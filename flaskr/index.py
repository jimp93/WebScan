from flask import (
    Blueprint, render_template, request, session
)
from flaskr.auth import login_required
import uuid
from flaskr.logic import start_logic
import json
import redis

r = redis.Redis(host='localhost', port=6379, charset="utf-8", decode_responses=True)

bp = Blueprint('index', __name__)


@bp.route('/changed', methods=('GET', 'POST'))
@login_required
def changed():
    job_id = session['job_id']
    add1 = r.hget(job_id, 'old_text')
    del1 = r.hget(job_id, 'new_text')

    a1 = add1[0:13]
    a2 = add1[-14:]
    chalen = 14+(len(add1)-28)
    cha = add1[13:chalen]

    d1 = del1[0:13]
    d2 = del1[-14:]
    chdlen = 14+(len(del1)-28)
    chd = del1[13:chdlen]

    r.delete(job_id)
    aud = session['audio']

    if add1 and del1:
        return render_template('index/changed.html', a1=a1, a2=a2, cha=cha, d1=d1, d2=d2, chd=chd, aud=aud,
                               deleted=del1, added=add1)
    if add1 and not del1:
        return render_template('index/changed.html', a1=a1, a2=a2, cha=cha,  d1='Nothing Deleted', d2="", chd="",
                               aud=aud)
    if add1 and not del1:
        return render_template('index/changed.html', a1='Nothing Added', a2="", cha="", d1=d1, d2=d2, chd=chd, aud=aud)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    return render_template('index/index.html')


@bp.route('/start', methods=['POST'])
def q_job():
    data = json.loads(request.data.decode())
    url = data["url"]
    numbers = data["numbers"]
    rtime = data["rtime"]
    session['audio'] = data["audio"]
    if url[0:3] != "htt":
        url = 'http://' + url
    # put job and queue, worker auto starts the job GOES ASYNC HERE, THIS FUNC CARRIES ON
    # returns jobid no, randomly generated
    jid = str(uuid.uuid4())
    job = start_logic.send(url, numbers, rtime, jid)
    return jid


@bp.route('/results', methods=['GET','POST'])
def get_results():
    data1 = json.loads(request.data.decode())
    job_id = data1["jobID"]
    r = redis.Redis(host='localhost', port=6379, charset="utf-8", decode_responses=True)
    t = r.hget(job_id, 'tagger')
    if t == 'change':
        session['job_id'] = job_id
        return 'go change'
    else:
        return "Nay!", 202




