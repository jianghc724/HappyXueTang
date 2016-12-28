from __future__ import absolute_import
from HappyXueTang.celery import app
from wechat.handlers import *
from wechat.wrapper import *
from wechat.models import *


@app.task(name='wechat.tasks.get_notice')
def get_notice():
    users = User.objects.all()
    for user in users:
        if user.user_status != 0:
            continue
        msg = "动态"
        for handler in WeChatView.handlers:
            inst = handler(WeChatView, msg, user)
            if inst.check():
                return inst.handle()
        return WeChatView.default_handler(WeChatView, msg, user).handle()