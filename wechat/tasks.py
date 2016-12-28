from __future__ import absolute_import
from HappyXueTang.celery import app
from wechat.handlers import *
from wechat.wrapper import *
from wechat.models import *
from datetime import datetime
from HappyXueTang.settings import WECHAT_APPID


@app.task(name='wechat.tasks.get_notice')
def get_notice():
    users = User.objects.all()
    for user in users:
        print(user)
        if user.user_status != 0:
            continue
        print(user)
        msg = {
            'FromUserName': user.open_id,
            'ToUserName': WECHAT_APPID,
            'MsgType':"text",
            'CreateTime': datetime.now().timestamp(),
            'Content': "动态",
        }
        for handler in WeChatView.handlers:
            inst = handler(WeChatView, msg, user)
            print(inst)
            if inst.check():
                print("in handler")
                return inst.handle()
        return WeChatView.default_handler(WeChatView, msg, user).handle()