from django.conf.urls import url

import user.views

# -*- coding: utf-8 -*-

urlpatterns = [
    url(r'^user/bind?$', user.views.UserBind.as_view()),
    url(r'^course/list?$', user.views.CourseList.as_view()),
<<<<<<< HEAD
    url(r'^course/detail?$', user.views.CourseDetail.as_view()),
    url(r'^course/comments/overview?$', user.views.CommentOverview.as_view()),
    url(r'^course/notices?$', user.views.GetNotice.as_view()),
=======
>>>>>>> parent of 3054fd4... Merge branch 'master' of github.com:jianghc724/HappyXueTang
    url(r'^ddl/list?$', user.views.GetDeadline.as_view()),
    url(r'^library/status?$', user.views.LibraryStatus.as_view()),
    url(r'^bullet/screen?$', user.views.BulletScreen.as_view()),
    url(r'^search/course?$', user.views.InfoSearch.as_view()),
]