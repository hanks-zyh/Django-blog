# -*- coding:utf-8 -*-

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render
from django.conf import settings
import logging
from models import Category, Article

logger = logging.getLogger('blog.views')


# Create your views here.
def global_setting(request):
    # 网站基本信息
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC

    # 导航栏分类数据
    category_list = Category.objects.all()[:5]
  
    # 推荐文章
    # 广告数据
    # Tag数据

    # 文章归档
    # 1. 获取文章月份的归档
    archive_list = Article.objects.distinct_date()
    return locals()


def index(request):
    try:
        article_list = Article.objects.all()
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())

def archive(request):
    try: 
        year = request.GET.get('year', None)
        mouth = request.GET.get('mouth', None)
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+mouth)
        article_list = getPage(request, article_list)
    except Exception, e:
        logger.error(e)
    return render(request, 'archive.html', locals())

def getPage(request, article_list):
    paginator = Paginator(article_list, 2)
    try:
        page = int(request.GET.get('page', 1 ))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list