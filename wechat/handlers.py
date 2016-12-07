from wechat.wrapper import WeChatHandler
from HappyXueTang import settings
from wechat.models import User
from django.http import HttpResponse

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
        print(user.user_status)
        return self.reply_text(self.get_message('unbind_account'))


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
