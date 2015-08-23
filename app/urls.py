#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.views import index,archive
from django.conf.urls import  url
urlpatterns = [

    url(r'^$', index, name='index'),
    url(r'^archive/$', archive, name='archive'),
]
