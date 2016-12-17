from wechat.wrapper import WeChatHandler
from HappyXueTang import settings
from wechat.models import *
from django.http import HttpResponse
from HappyXueTang.settings import API_KEY, API_SECRET
from codex.baseerror import *
from datetime import datetime
import requests, json


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('我爱学习,学习使我快乐~随便看看吧~')


class HelpOrSubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('帮助', 'help') or self.is_event('scan', 'subscribe')

    def handle(self):
        '''return self.reply_single_news({
            'Title': self.reply_text('帮助'),
            'Description': self.get_message('help'),
            'Url': pass
        })'''
        pass


class UnbindOrUnsubscribeHandler(WeChatHandler):
    def check(self):
        return self.is_text('解绑')

    def handle(self):
        if self.user.user_id == '' or self.user.user_status == -1:
            return self.reply_text("对不起，您还未绑定账号")
        user = User.get_by_openid(self.user.open_id)
        user.user_status = -1
        user.save()
        data = {
            "apikey": API_KEY,
            "apisecret": API_SECRET,
        }
        headers = {'content-type': 'application/json'}
        userid = User.get_by_openid(self.user.open_id).user_id
        addr = 'http://se.zhuangty.com:8000/users/' + userid + '/cancel?username=' + userid
        print(addr)
        r = requests.post(addr, data=json.dumps(data), headers=headers)
        print(r)
        print(r.json())
        return_json = r.json()
        if return_json['message'] == 'Success':
            return self.reply_text(self.get_message('unbind_account'))
        else:
            raise LogicError("UnBind Failure")


class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_text('绑定') or self.is_event_click(self.view.event_keys['account_bind'])

    def handle(self):
        return self.reply_text(self.get_message('bind_account'))


class CourseDetailHandler(WeChatHandler):
    def check(self):
        return self.is_text('课程')

    def handle(self):
        pass


class CourseListHandler(WeChatHandler):

    def check(self):
        return self.is_text('课程表') or self.is_event_click(self.view.event_keys['get_curriculum_schedule'])

    def handle(self):
        if self.user.user_id == '' or self.user.user_status == -1:
            return self.reply_text(self.get_message('bind_account'))
        return self.reply_text(self.get_message('list'))


class BulletScreenHandler(WeChatHandler):

    def check(self):
        return self.is_text_command('弹幕') or self.is_event_click(self.view.event_keys['bullet_screen'])

    def handle(self):
        dict = self.input['Content'].split(' ')
        student_id = self.user.user_id
        course_k_a_n = dict[1]
        course_detail = dict[1].split('-')
        course_key = course_detail[0]
        course_number = course_detail[10]
        bullet_content = dict[2]
        current_time = datetime.now().timestamp()
        dis = Discussion.objects.create(student_id=student_id, course_key=course_key, course_number = course_number,
                                        content=bullet_content, status=False, release_time=current_time)
        dis.save()
        return self.reply_text(self.get_message('class_talk'))