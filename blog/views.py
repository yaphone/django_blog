#coding=utf-8

from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from blogParser import parser
import time
import os
import json
BASE_DIR = os.path.dirname(__file__)

from .models import Blog

# Create your views here.
def index(request):
    blog_list = Blog.objects.order_by('-update_time')[:5]
    context = {'blog_list': blog_list}
    return render(request, 'blog/index.html', context)


@login_required
def publish(request):
    return render(request, 'blog/publish.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/blog/')


@csrf_exempt
def auth(request):
    username = request.POST.get("username", "null")
    password = request.POST.get("password", "null")
    next_url = request.POST.get("next")
    #logout(request)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(next_url)

    else:
        return JsonResponse({'status':'error'})

def publish_article(request):
    title = request.POST.get("title", "null")
    classify = request.POST.get("classify", "null")
    tag = request.POST.get("keywords", "null")
    content = request.POST.get("content", "null")
    update_time = time.time()
    blog = Blog(blog_title = title, blog_content=content, update_time = timezone.now(), 
                modify_time = timezone.now(), blog_tag = tag, blog_type = classify)
    blog.save()
    return HttpResponseRedirect('/blog/')
    
def detail(request):
    title = request.GET.get("title")
    blog_list = Blog.objects.filter(blog_title = title)
    context = {'blog_list': blog_list}
    return render(request, 'blog/detail.html', context)

'''
def get_markdowns(request):
    md_path = os.path.join(BASE_DIR, 'static/markdowns')
    md_list = os.listdir(md_path)
    print md_list
    return HttpResponse(md_list)
'''

#返回所有的markdown文件页面
@login_required
def markdowns(request):
    return render(request, 'blog/markdown.html')

@login_required
def get_md_info(request):
    md_path = os.path.join(BASE_DIR, 'static/markdowns')
    md_list = os.listdir(md_path)
    md_info_dict = {}  # 存储所有的markdown文件名，转为json对象时使用
    md_info_list = []  # 存储md文件信息列表
    for md in md_list:
        md_info = {}  # 存储单个md信息
        md_info.setdefault('mdName', md)
        md_info_list.append(md_info)
    md_info_dict.setdefault('md', md_info_list)
    return JsonResponse(md_info_dict, safe=False)


#根据前端传来的markdown文件名列表将文件解析并插入数据库
@login_required
def get_md_name_list(request):
    md_name_list_str = request.GET['md_name_list']
    md_name_list = md_name_list_str.split(',')
    for md_name in md_name_list:
        file_path = os.path.join(BASE_DIR, 'static/markdowns/' + md_name)
        blog_dict = parser(file_path)
        title = blog_dict['title']
        classify = blog_dict['classify']
        keywords = blog_dict['keywords']
        content = blog_dict['content']
        blog = Blog(blog_title=title, blog_content=content, update_time=timezone.now(),
                    modify_time=timezone.now(), blog_tag=keywords, blog_type=classify)
        blog.save()
    return HttpResponse(request)

