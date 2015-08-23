# -*- coding:utf-8 -*-

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render
from django.conf import settings
from django.db.models import Count
import logging
from models import Category, Article, Comment, Tag

logger = logging.getLogger('blog.views')


# Create your views here.
def global_setting(request):
    # 网站基本信息
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC

    # 导航栏分类数据
    category_list = Category.objects.all()[:5]
  


    # 广告数据
    # Tag数据

    # 文章归档
    # 1. 获取文章月份的归档
    archive_list = Article.objects.distinct_date()

    # 评论排行
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')[:6]
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    
    # 浏览排行
    article_click_list = Article.objects.order_by('-click_count')[:6]
    # 站长推荐
    article_recomment_list = Article.objects.filter(is_recommend=True)[:6]

    #标签云数据
    tag_list = Tag.objects.all()

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

def tag(request):
    try:
        tag_name = request.GET.get('tag',None)
        article_list = Article.objects.filter(tag__name=tag_name)
        article_list = getPage(request, article_list)
    except Exception, e:
        logger.error(e)
    return render(request, 'tag.html', locals())


def getPage(request, article_list):
    paginator = Paginator(article_list, 2)
    try:
        page = int(request.GET.get('page', 1 ))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list


