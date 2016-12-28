from __future__ import absolute_import

from HappyXueTang.celery import app
from wechat.models import *
from HappyXueTang.settings import API_SECRET, API_KEY

import requests
import json


@app.task
def get_notice_task():
    users = User.objects.all()
    for user in users:
        if user.user_status != 0:
            continue
        userid = user.user_id
        data = {
            "apikey": API_KEY,
            "apisecret": API_SECRET,
        }
        headers = {'content-type': 'application/json'}
        addr = 'http://se.zhuangty.com:8000/learnhelper/' + userid + '/courses?username=' + userid
        r = requests.post(addr, data=json.dumps(data), headers=headers)
        return_json = r.json()
        if return_json['message'] == 'Success':
            total_notice = 0
            total_homework = 0
            course_json = return_json['courses']
            for course in course_json:
                total_homework = total_homework + course['unsubmittedopertions']
                total_notice = total_notice + course['unreadnotice']
            result = {
                'notices': total_notice,
                'homework': total_homework,
            }
    # print ("celery work")
    pass
