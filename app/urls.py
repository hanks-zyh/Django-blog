#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.views import index, archive, tag, article, comment_post, category, do_reg, do_login, do_logout
from django.conf.urls import  url
urlpatterns = [

    url(r'^$', index, name='index'),
    url(r'^archive/$', archive, name='archive'),
    url(r'^tag/$', tag, name='tag'),
    url(r'^article/$', article, name='article'),
    url(r'^comment/post/$', comment_post, name='comment_post'),
    url(r'^logout$', do_logout, name='logout'),
    url(r'^reg', do_reg, name='reg'),
    url(r'^login', do_login, name='login'),
    url(r'^category/$', category, name='category'),
]
