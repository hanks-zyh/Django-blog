#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.views import index, archive, tag
from django.conf.urls import  url
urlpatterns = [

    url(r'^$', index, name='index'),
    url(r'^archive/$', archive, name='archive'),
    url(r'^tag/$', tag, name='tag'),
]
