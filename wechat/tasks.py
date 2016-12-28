from __future__ import absolute_import
import logging
from HappyXueTang.celery import app
from celery.utils.log import get_task_logger
from wechat.handlers import *
from wechat.wrapper import *
from wechat.models import *
from datetime import datetime
from HappyXueTang.settings import WECHAT_APPID


@app.task(name='wechat.tasks.get_notice')
def get_notice():
    logger = get_task_logger(__name__)
    logger.info('func start  ----------------->')
    users = User.objects.all()
    for user in users:
        if user.user_status != 0:
            continue
        msg = {
            'FromUserName': user.open_id,
            'ToUserName': WECHAT_APPID,
            'MsgType':"text",
            'CreateTime': datetime.now().timestamp(),
            'Content': "动态",
        }
        for handler in WeChatView.handlers:
            inst = handler(WeChatView, msg, user)
            if inst.check():
                inst.handle()
        logger.info('func end  ----------------->')