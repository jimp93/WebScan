from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, Response, stream_with_context
)
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.logic import make_ad_dic
import requests
import time
from bs4 import BeautifulSoup

bp = Blueprint('index', __name__)


@bp.route('/changed', methods=('GET', 'POST'))
@login_required
def changed():
    db = get_db()
    add = db.execute(
        'SELECT old_text FROM texts'
    ).fetchone()
    delete = db.execute(
        'SELECT new_text FROM texts'
    ).fetchone()
    add1 = add[0]
    del1 = delete[0]
    db.execute("delete from texts")
    db.commit()
    if add1 and del1:
        return render_template('index/changed.html', added=add1, deleted=del1)
    if add1 and not del1:
        return render_template('index/changed.html', added=add1, deleted='Nothing Deleted')
    if add1 and not del1:
        return render_template('index/changed.html', added='Nothing Added', deleted=del1)


#VERY GOOD - allows to render a template and then do stuff in the background, use yield instead of return
@bp.route('/searching', methods=('GET', 'POST'))
@login_required
def search():
    if request.method == 'POST':
        log = make_ad_dic
        new_text = []
        old_text = []
        webpage = session['webpage']
        rtime = session['rtime']
        while True:
            headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            response = requests.get(webpage, headers=headers)# gets webpage using differnt browsers
            soup = BeautifulSoup(response.text, features="html.parser")#returns the whole page
            for script in soup(["script", "style"]):  # remove all javascript and stylesheet code
                script.extract()
            text = soup.get_text()#gets text of what is left
            lines = (line.strip() for line in text.splitlines())# breaks block into lines where \ and removes leading and trailing space on each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))# break multi-headlines into a line each
            text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
            new_text.append(text)
            if old_text:
                if new_text != old_text:
                    # db = get_db()
                    # db.execute("delete from texts")
                    # db.commit()
                    # db.execute('INSERT INTO texts (old_text, new_text) VALUES (?, ?)', (old_text[0], new_text[0]))
                    # db.commit()
                    log(old_text[0], new_text[0])
                    if session['tagger'] == 'change':
                        break
            old_text = []
            old_text.append(text)
            new_text = []
            rtime = int(rtime)
            time.sleep(10)
        return 'done'
    return render_template('index/searching.html')


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST':
        webpage = request.form['website']
        rtime = request.form['time']
        rnum = request.form['numbers']
        if webpage[0] != 'h':
            webpage = 'http://' + webpage
        db = get_db()
        g.user_mail = db.execute(
            'SELECT email FROM user WHERE id = ?', (session['user_id'],)
        ).fetchone()
        error = None
        session['webpage'] = webpage
        session['rtime'] = rtime
        session['numbers'] = rnum
        try:
            myrequest = requests.get(session['webpage'])
            return redirect(url_for('.search'))
        except:
            error = 'Enter valid webpage'
            flash(error)
    return render_template('index/index.html')


def del_difference(old_list, new_list):
    return (list(set(old_list) - set(new_list)))


def add_difference(new_list, old_list):
    return (list(set(new_list) - set(old_list)))




