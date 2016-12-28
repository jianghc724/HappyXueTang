from django.conf.urls import url

import user.views

# -*- coding: utf-8 -*-

urlpatterns = [
    url(r'^user/bind?$', user.views.UserBind.as_view()),
    url(r'^course/list?$', user.views.CourseList.as_view()),
    url(r'^course/detail?$', user.views.CourseDetail.as_view()),
    url(r'^course/comments/overview?$', user.views.CommentsOverview.as_view()),
    url(r'^ddl/list?$', user.views.GetDeadline.as_view()),
    url(r'^library/status?$', user.views.LibraryStatus.as_view()),
    url(r'^bullet/screen?$', user.views.BulletScreen.as_view()),
]