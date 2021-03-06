from __future__ import absolute_import
from HappyXueTang.celery import app
from wechat.handlers import *
from wechat.wrapper import *
from wechat.models import *
from wechat.views import CustomWeChatView
from datetime import datetime
from HappyXueTang.settings import WECHAT_APPID, WECHAT_SECRET


@app.task(name='wechat.tasks.get_notice')
def get_notice():
    users = User.objects.all()
    for user in users:
        print(user.user_id)
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
                print(course)
                total_homework = total_homework + course['unsubmittedoperations']
                total_notice = total_notice + course['unreadnotice']
            ac_addr = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="\
                      + WECHAT_APPID + "&secret=" + WECHAT_SECRET
            r = requests.get(ac_addr)
            # print(r)
            access_json = r.json()
            # print(access_json)
            access_token = access_json['access_token']
            return_str = "Notices:" + str(total_notice) + " Homework:" + str(total_homework)
            print (return_str)
            we_addr = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=" + access_token
            we_data = {
                "touser": user.open_id,
                "msgtype": "text",
                "text":
                    {
                        "content": return_str
                    }

            }
            r = requests.post(we_addr, data=json.dumps(we_data, ensure_ascii=False))
            print(r)