from django.conf.urls import url

import user.views

# -*- coding: utf-8 -*-

urlpatterns = [
    url(r'^user/bind?$', user.views.UserBind.as_view()),
    url(r'^course/list?$', user.views.CourseList.as_view()),
]