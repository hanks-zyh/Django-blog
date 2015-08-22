# -*- coding:utf-8 -*-

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render
from django.conf import settings
import logging
from models import Category, Article

logger = logging.getLogger('blog.views')


# Create your views here.
def global_setting(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESC': settings.SITE_DESC,
    }


def index(request):
    try:
        # 最新文章数据
        category_list = Category.objects.all()[:5]
        article_list = Article.objects.all()
        paginator = Paginator(article_list, 2)
        try:
            page = int(request.GET.get('page', 1 ))
            article_list = paginator.page(page)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            article_list = paginator.page(1)

        # 文章归档
        # 1. 获取文章月份的归档
        archive_list = Article.objects.distinct_date()
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())
