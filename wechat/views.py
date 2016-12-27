from django.utils import timezone

from wechat.wrapper import WeChatView, WeChatLib
from wechat.models import User
from wechat.handlers import *
from HappyXueTang.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET, get_url


class CustomWeChatView(WeChatView):

    lib = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET)

    handlers = [
        UnbindOrUnsubscribeHandler, BindAccountHandler, CourseListHandler,
        BulletScreenHandler, DDLCenterHandler
    ]

    error_message_handler = ErrorHandler
    default_handler = DefaultHandler
    #SITE_DOMAIN = "http://59.66.250.60/"

    event_keys = {
        'get_curriculum_schedule': 'SERVICE_GET_CURRICULUM_SCHEDULE',
        'get_ddl': 'SERVICE_GET_DDL',
        'get_exam_info': 'SERVICE_GET_EXAM_INFO',
        'get_new_trend': 'SERVICE_GET_NEW_TREND',
        'account_bind': 'SERVICE_BIND',
        'bullet_screen': 'SERVICE_BULLET_SCREEN',
        'lecture_bbs': 'SERVICE_LECTURE_BBS',
        'get_library': 'SERVICE_GET_LIBRARY',
        'search_lecture': 'SERVICE_SEARCH_LECTURE',
        'xuetang_achievement': 'SERVICE_XUETANG_ACHIEVEMENT',
    }

    menu = {
        'button': [
            {
                "name": "我的课程",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "课程表",
                        "url": settings.get_url('student/course_list', {'open_id': WeChatView.wechatUser.open_id})
                    },
                    {
                        "type": "view",
                        "name": "DDL中心",
                        "url": settings.get_url('student/ddl_center', {'open_id': WeChatView.wechatUser.open_id})
                    },
                    {
                        "type": "click",
                        "name": "新动态",
                        "key": event_keys['get_new_trend'],
                    },
                    {
                        "type": "click",
                        "name": "考试信息",
                        "key": event_keys['get_exam_info'],
                    },
                    {
                        "type": "click",
                        "name": "账号绑定",
                        "key": event_keys['account_bind'],
                    }
                ]
            },
            {
                "name": "课程互动",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "课聊",
                        "key": event_keys['bullet_screen'],
                    },
                    {
                        "type": "click",
                        "name": "课程论坛",
                        "key": event_keys['lecture_bbs'],
                    }
                ]
            },
            {
                "name": "学习助手",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "我要自习",
                        "key": event_keys['get_library'],
                    },
                    {
                        "type": "click",
                        "name": "我要搜课",
                        "key": event_keys['search_lecture'],
                    },
                    {
                        "type": "click",
                        "name": "学堂成就",
                        "key": event_keys['xuetang_achievement'],
                    }
                ]
            }
        ]
    }

    @classmethod
    def update_menu(cls):
        cls.lib.set_wechat_menu(cls.menu)
