from __future__ import absolute_import
from HappyXueTang.celery import app
from wechat.wrapper import WeChatHandler
from HappyXueTang.settings import API_SECRET, API_KEY

import requests
import json

@app.task
def get_notice(WeChatHandler):
    userid = WeChatHandler.user.user_id
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
            print (course)
            total_homework = total_homework + course['unsubmittedoperations']
            total_notice = total_notice + course['unreadnotice']
        return WeChatHandler.reply_text("您还有" + str(total_notice) + "个未读公告，" + str(total_homework) + "个未交作业")