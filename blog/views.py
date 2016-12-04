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
    blog_show_num = 5  #每页显示文章数目
    show_start = 0;
    show_end = 5
    page_no = 0  #当前页数
    try:
        page_no = int(request.GET['page_no'])
    except:
        pass
    show_start = page_no * blog_show_num
    show_end = show_start + 5
    blog_list = Blog.objects.order_by('-update_time')[show_start:show_end]
    context = {'blog_list': blog_list, 'page_no': page_no}
    return render(request, 'blog/index.html', context)

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

    
def detail(request):
    title = request.GET.get("title")
    blog_list = Blog.objects.filter(blog_title = title)
    context = {'blog_list': blog_list}
    return render(request, 'blog/detail.html', context)


#返回所有的markdown文件页面
@csrf_exempt
@login_required
def markdowns(request):
    if request.method == 'POST':
        md_name_list_str = request.POST.get('md_name_list')
        md_name_list = md_name_list_str.split(',')
        blog_list = Blog.objects.order_by('-update_time')
        blog_title_list = [blog.blog_title for blog in blog_list]
        for md_name in md_name_list:
            if md_name in blog_title_list:
                blog = Blog.objects.get(blog_title=md_name)
                blog_id = blog.id
            else:
                blog_id = None
            file_path = os.path.join(BASE_DIR, 'static/markdowns/' + md_name + '.md')
            blog_dict = parser(file_path)
            title = blog_dict['title']
            classify = blog_dict['classify']
            keywords = blog_dict['keywords']
            content = blog_dict['content']
            blog = Blog(id=blog_id, blog_title=title, blog_content=content, update_time=timezone.now(),
                        modify_time=timezone.now(), blog_tag=keywords, blog_type=classify)
            blog.save()
        return JsonResponse({'status': 'OK'})
    if request.method == 'GET':
        return render(request, 'blog/markdown.html')

#返回所有的md文件名
@csrf_exempt
@login_required
def get_md_info(request):
    md_path = os.path.join(BASE_DIR, 'static/markdowns')
    md_list = os.listdir(md_path)
    md_info_dict = {}  # 存储所有的markdown文件名，转为json对象时使用
    md_info_list = []  # 存储md文件信息列表
    for md in md_list:
        md_info = {}  # 存储单个md信息
        md_info.setdefault('mdName', md[:len(md)-3]) #去掉'md'后缀
        md_info_list.append(md_info)
    md_info_dict.setdefault('md', md_info_list)
    return JsonResponse(md_info_dict, safe=False)


@csrf_exempt
@login_required
def delete(request):
    if request.method == "POST":
        blog_titles = request.POST.get('title_list')
        print blog_titles
        if blog_titles:
            blog_title_list = blog_titles.split(',')
            for title in blog_title_list:
                blog = Blog.objects.get(blog_title=title)
                blog.delete()
            return JsonResponse({'status': 'OK'})
    if request.method == "GET":
        return render(request, 'blog/delete.html')

#返回所有的博客标题
@login_required
def get_all_title_info(request):
    blog_list = Blog.objects.order_by('-update_time')
    blog_title_list = [blog.blog_title for blog in blog_list]
    title_dict = {}
    title_info_list = []
    for blog_title in blog_title_list:
        title_info = {'title': blog_title}
        title_info_list.append(title_info)
    title_dict.setdefault('blog_titles', title_info_list)
    return JsonResponse(title_dict, safe=False)


@csrf_exempt
@login_required
def upload(request):
    if request.method == "POST":
        md = request.FILES.get('md')
        print md
        if md:
            mdFile = open(os.path.join(BASE_DIR, 'static/markdowns/' + md.name), 'wb+')
            mdFile.write(md.read())
            mdFile.close()
    return render(request, 'blog/upload.html')












