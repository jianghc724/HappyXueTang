from __future__ import absolute_import

from HappyXueTang.celery import app

@app.task
def get_notice_task():

    # print ("celery work")
    pass
