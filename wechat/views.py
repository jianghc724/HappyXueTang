from django.utils import timezone

from wechat.wrapper import WeChatView, WeChatLib
from wechat.handlers import *
from HappyXueTang.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET


class CustomWeChatView(WeChatView):

    lib = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET)

    handlers = [
        DefaultHandler,
        ErrorHandler,
        BindAccountHandler,
        UnbindOrUnsubscribeHandler,
        CourseDetailHandler,
    ]
    error_message_handler = ErrorHandler
    default_handler = DefaultHandler

    event_keys = {

    }

    menu = {

    }
