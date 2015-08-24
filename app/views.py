# -*- coding:utf-8 -*-
from django.contrib.auth import login, authenticate, logout

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Count
import logging
from models import Category, Article, Comment, Tag, Links, User
from forms import CommentForm, LoginForm, RegForm

logger = logging.getLogger('blog.views')


# Create your views here.
def global_setting(request):
    # 网站基本信息
    SITE_URL = settings.SITE_URL
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
    comment_count_list = Comment.objects.values('article').annotate(
        comment_count=Count('article')).order_by('-comment_count')[:6]
    article_comment_list = [
        Article.objects.get(pk=comment['article']) for comment in comment_count_list]

    # 浏览排行
    article_click_list = Article.objects.order_by('-click_count')[:6]
    # 站长推荐
    article_recomment_list = Article.objects.filter(is_recommend=True)[:6]

    # 标签云数据
    tag_list = Tag.objects.all()[:30]

    # 友情链接
    link_list = Links.objects.all()[:5]
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
        article_list = Article.objects.filter(
            date_publish__icontains=year + '-' + mouth)
        article_list = getPage(request, article_list)
    except Exception, e:
        logger.error(e)
    return render(request, 'archive.html', locals())


def tag(request):
    try:
        tag_name = request.GET.get('tag', None)
        article_list = Article.objects.filter(tag__name=tag_name)
        article_list = getPage(request, article_list)
    except Exception, e:
        logger.error(e)
    return render(request, 'tag.html', locals())


def article(request):
    try:
        # 获取文章id
        article_id = request.GET.get('id', None)
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'resion': '没有找到对应文章'})
        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': article_id} if request.user.is_authenticated() else{
            'article': article_id})
        # 获取评论列表
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:  # 这条评论是item的子级评论
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:  # 父级评论
                comment_list.append(comment)

    except Exception, e:
        logger.error(e)
    return render(request, 'article.html', locals())


# 提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # 获取表单信息
            comment = Comment(username=comment_form.cleaned_data["author"],
                              email=comment_form.cleaned_data["email"],
                              url='http://csdi.com',
                              content=comment_form.cleaned_data["comment"],
                              article_id=comment_form.cleaned_data["article"],
                              user=request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        print  e
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


def getPage(request, article_list):
    paginator = Paginator(article_list, 2)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list


# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print e
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                from django.contrib.auth.hashers import make_password
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                           email=reg_form.cleaned_data["email"],
                                           url=reg_form.cleaned_data["url"],
                                           password=make_password(reg_form.cleaned_data["password"]), )
                user.save()

                # 登录
                # 指定默认的登录验证方式
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())


# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    # 指定默认的登录验证方式
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        print  e
        logger.error(e)
    return render(request, 'login.html', locals())


def category(request):
    try:
        # 先获取客户端提交的信息
        cid = request.GET.get('cid', None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:
            return render(request, 'failure.html', {'reason': '分类不存在'})
        article_list = Article.objects.filter(category=category)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())
