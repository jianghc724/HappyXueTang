from wechat.wrapper import WeChatHandler


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
        pass


class BindAccountHandler(WeChatHandler):
    def check(self):
        return self.is_text('绑定')

    def handle(self):
        pass


class CourseDetailHandler(WeChatHandler):
    def check(self):
        return self.is_text('课程')

    def handle(self):
        pass