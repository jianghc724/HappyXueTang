from wechat.wrapper import WeChatHandler
from HappyXueTang import settings

class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')


class UnbindOrUnsubscribeHandler(WeChatHandler):
    def check(self):
        return self.is_text('解绑')

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')



class BindAccountHandler(WeChatHandler):
    def url_bind(self):
        return settings.get_url('u/bind', {'open_id':self.user.open_id})

    def check(self):
        print("adsf")
        return self.is_text('绑定') or self.is_event_click(self.view.event_keys['account_bind'])

    def handle(self):
        return self.reply_text(self.get_message('bind_account'))


class CourseDetailHandler(WeChatHandler):
    def check(self):
        return self.is_text('课程')

    def handle(self):
        pass