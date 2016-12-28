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
        inst = GetNewNoticeHandler(WeChatView, "动态", user)
        inst.handle()