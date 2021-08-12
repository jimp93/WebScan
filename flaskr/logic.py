# -*- coding:utf-8 -*-
import difflib
import requests
from bs4 import BeautifulSoup
import time
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results.backends import RedisBackend
from dramatiq.results import Results
import redis


redis_ = redis.Redis(host='localhost', port=6379, charset="utf-8", decode_responses=True)
result_backend = RedisBackend(url="redis://127.0.0.1:6379")
broker = RedisBroker(url="redis://127.0.0.1:6379")
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)


def fill_db(ready_a, ready_d, job_id):
    old_text = ready_a[0]
    new_text = ready_d[0]
    redis_.hset(job_id, 'old_text', old_text)
    redis_.hset(job_id, 'new_text', new_text)


def realise_real_chunks(old_d, new_d, keys_to_realise_a, keys_to_realise_d, real_spansa, real_spoansd, job_id):
    full_filt_dic_o = {}
    full_filt_dic_n = {}
    final_add_ex = []
    final_del_ex = []
    final_add_real = []
    final_del_real = []

    for key in old_d:
        full_filt_dic_o[key] = old_d[key][2]

    for key in new_d:
        full_filt_dic_n[key] = new_d[key][2]

    real_add = []
    extended_add = []

    real_del = []
    extended_del = []

    for ka in keys_to_realise_a:
        carrier_a = []
        for kaa in ka:
            carrier_a.append(full_filt_dic_n[kaa])
        extended_add.append(carrier_a)

    for kd in keys_to_realise_d:
        carrier_d = []
        for kdd in kd:
            carrier_d.append(full_filt_dic_o[kdd])
        extended_del.append(carrier_d)

    for ra in real_spansa:
        carrier_ra = []
        for kraa in ra:
            carrier_ra.append(full_filt_dic_n[kraa])
        real_add.append(carrier_ra)

    for rd in real_spoansd:
        carrier_rd = []
        for krdd in rd:
            carrier_rd.append(full_filt_dic_o[krdd])
        real_del.append(carrier_rd)

    for raa in real_add:
        ta = "".join(raa)
        final_add_real.append(ta)

    for rdd in real_del:
        da = "".join(rdd)
        final_del_real.append(da)

    for edd in extended_del:
        sa = "".join(edd)
        final_del_ex.append("... " + str(sa) + " ...")

    for ead in extended_add:
        ram = "".join(ead)
        final_add_ex.append("... " + str(ram) + " ...")

    fill_db(final_add_ex, final_del_ex, job_id)
    redis_.hset(job_id, 'tagger', 'change')


def realise_keys(string_ld, string_la, add_no, del_no, new_d, old_d, job_id):
    keys_to_realise_a = []
    keys_to_realise_d = []
    real_spansa = []
    real_spansd = []
    stt = 0

    for la in string_la:
        ct = 0
        cr = 0
        in_list = []
        rin_list = []
        ste = stt + (la - 1)
        tas = add_no[stt]
        tae = add_no[ste]
        numbers = tae - tas
        for r in range(numbers + 1):
            xr = tas + cr
            if xr >= 0:
                if xr == len(new_d):
                    break
                rin_list.append(xr)
            cr += 1
        real_spansa.append(rin_list)

        for r in range(numbers + 20):
            xx = (tas - 9) + ct
            if xx >= 0:
                if xx == len(new_d):
                    break
                in_list.append(xx)
            ct += 1
        stt += la
        keys_to_realise_a.append(in_list)

    std = 0
    for ld in string_ld:
        ctd = 0
        crd = 0
        din_list = []
        drin_list = []
        sted = std + (ld - 1)
        tad = del_no[std]
        taed = del_no[sted]
        dnumbers = taed - tad

        for dr in range(dnumbers + 1):
            dxr = tad + crd
            if dxr >= 0:
                if dxr == len(old_d):
                    break
                drin_list.append(dxr)
            crd += 1
        real_spansd.append(drin_list)

        for d in range(dnumbers + 20):
            dxx = (tad - 9) + ctd
            if dxx >= 0:
                if dxx == len(old_d):
                    break
                din_list.append(dxx)
            ctd += 1
        std += ld
        keys_to_realise_d.append(din_list)
    realise_real_chunks(old_d, new_d, keys_to_realise_a, keys_to_realise_d, real_spansa, real_spansd, job_id)


def chunk_limits(r_p, new_dic, old_dic, new_d, old_d, job_id):

    # works out limits of change chunks, for actual (ie to work out if just numbers) and for presenting extended
    #  and filled chunks

    def evaluate():
        if redis_.hget(job_id, 'numbers') == 'no':
            a_chunked = []
            d_chunked = []
            afirst = 0
            dfirst = 0
            all_no_a_constructor = []
            all_no_d_constructor = []

            if string_la:
                for sl in string_la:
                    asecond = afirst + sl
                    a_chunked.append(add_nov[afirst: asecond])
                    afirst = asecond

            if string_ld:
                for dl in string_ld:
                    dsecond = dfirst + dl
                    d_chunked.append(del_nov[dfirst: dsecond])
                    dfirst = dsecond

            for ra in a_chunked:
                if ra:
                    comparer_a = []
                    ct = 0
                    for raa in ra:
                        zzmin = ct - 1
                        zzplu = ct + 1
                        if raa.isdigit():
                            comparer_a.append(raa)
                        if raa == ',' or raa == ':' or raa == 'h':
                            if ct > 0 and ra[zzmin].isdigit():
                                comparer_a.append(raa)
                            if zzplu < len(ra):
                                if ra[zzplu].isdigit():
                                    comparer_a.append(raa)
                        ct += 1
                    if len(ra) == len(comparer_a):
                        all_no_a_constructor.append(ra)

            for rd in d_chunked:
                if rd:
                    comparer_d = []
                    cd = 0
                    for rdd in rd:
                        ddmin = cd - 1
                        ddplu = cd + 1
                        if rdd.isdigit():
                            comparer_d.append(rdd)
                        if rdd == ',' or rdd == ':':
                            if cd > 0 and rd[ddmin].isdigit():
                                comparer_d.append(rdd)
                        if ddplu < len(rd):
                            if rd[ddplu].isdigit():
                                comparer_d.append(rdd)
                        cd += 1
                    if len(rd) == len(comparer_d):
                        all_no_d_constructor.append(rd)

            if all_no_a_constructor:
                for ita in all_no_a_constructor:
                    if ita in a_chunked:
                        x = a_chunked.index(ita)
                        a_chunked.pop(x)
            if all_no_d_constructor:
                for itd in all_no_d_constructor:
                    if itd in d_chunked:
                        y = d_chunked.index(itd)
                        d_chunked.pop(y)

            if d_chunked or a_chunked:
                chunk_limits('p', new_dic, old_dic, new_d, old_d, job_id)

            else:
                print('no')
                redis_.hset(job_id, 'tagger', 'carry_on')

        else:
            chunk_limits('p', new_dic, old_dic, new_d, old_d, job_id)

    string_la = []
    string_ld = []
    aind = 1
    aindm = 0
    acounter = 1
    add_no = list(new_dic.keys())
    del_no = list(old_dic.keys())
    add_nov = list(new_dic.values())
    del_nov = list(old_dic.values())
    if r_p == 'r':
        pr = 1
    if r_p == 'p':
        pr = 5

    al = len(add_no) - 1
    all = al - 1

    if al > 0:
        for a in range(al):
            if add_no[aind] - add_no[aindm] <= pr:
                acounter += 1
            if add_no[aind] - add_no[aindm] > pr:
                string_la.append(acounter)
                acounter = 1
            if a == all:
                string_la.append(acounter)
            aind += 1
            aindm += 1
    else:
        string_la.append(1)

    dind = 1
    dindm = 0
    dcounter = 1

    dl = len(del_no) - 1
    dll = dl - 1

    if dl > 0:
        for d in range(dl):
            if del_no[dind] - del_no[dindm] <= pr:
                dcounter += 1
            if del_no[dind] - del_no[dindm] > pr:
                string_ld.append(dcounter)
                dcounter = 1
            if d == dll:
                string_ld.append(dcounter)
            dind += 1
            dindm += 1
    else:
        string_ld.append(1)

    if r_p == 'r':
        evaluate()
    if r_p == 'p':
        realise_keys(string_ld, string_la, add_no, del_no, new_d, old_d, job_id)


def make_ad_dic(old_text, new_text, job_id):
    # make dic of added, deleted chars and their position

    hmm = {}
    deleted = []
    added = []
    for i, s in enumerate(difflib.ndiff(old_text, new_text)):
        hmm[i] = s
        if s[0] == ' ':
            continue
        elif s[0] == '-':
            deleted.append(s[-1])
        elif s[0] == '+':
            added.append(s[-1])
    old_d = {}
    new_d = {}
    old_dic = {}
    new_dic = {}
    cd = 0
    ca = 0

    for dd in hmm:
        if hmm[dd][0] == " " or hmm[dd][0] == "-":
            old_d[cd] = hmm[dd]
            cd += 1
        if hmm[dd][0] == " " or hmm[dd][0] == "+":
            new_d[ca] = hmm[dd]
            ca += 1

    if old_d:
        for ddd in old_d:
            if old_d[ddd][0] == "-":
                old_dic[ddd] = old_d[ddd][2]

    if new_d:
        for eee in new_d:
            if new_d[eee][0] == "+":
                new_dic[eee] = new_d[eee][2]

    chunk_limits('r', new_dic, old_dic, new_d, old_d, job_id)


@dramatiq.actor
def start_logic(url, numbers, rrtime, jid):
    job_id=jid
    redis_.hset(job_id, 'numbers', numbers)
    redis_.hset(job_id, 'tagger', 'no_change')
    new_text = []
    old_text = []
    while True:
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)# gets webpage using differnt browsers
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
                make_ad_dic(old_text[0], new_text[0], job_id)
                if redis_.hget(job_id, 'tagger') == 'change':
                    break
        old_text = []
        old_text.append(text)
        new_text = []
        rtime = int(rrtime)
        time.sleep(rtime)
    return 'done'


