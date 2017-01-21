#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from blogParser import parser
from collections import Counter
import time
import os
import platform
import json
BASE_DIR = os.path.dirname(__file__)

from .models import Blog, Comment, SubComment

# Create your views here.
def index(request):
    blog_show_num = 5  #每页显示文章数目
    page_no = 0  #当前页数
    try:
        page_no = int(request.GET['page_no'])
    except:
        pass
    show_start = page_no * blog_show_num
    show_end = show_start + 5
    all_blog_list = Blog.objects.order_by('-update_time')
    latest_blog_list = Blog.objects.order_by('-modify_time')
    sum_blog = len(all_blog_list) #博文总数，分页使用
    is_last_page = 'false' #判断当前是否是最后一页
    # 最近十篇文章
    if sum_blog >= 10:
        latest_blog_title_list = [blog.blog_title for blog in latest_blog_list[:10]]
    else:
        latest_blog_title_list = [blog.blog_title for blog in latest_blog_list[:sum_blog]]
    # 归档分类
    classify_list = [blog.blog_type for blog in all_blog_list]
    classify_dict = dict(Counter(classify_list))

    if blog_show_num * (page_no + 1) >= sum_blog:  #判断是否在最后一页
        is_last_page = 'true'
    blog_list = all_blog_list[show_start:show_end]
    #搜索功能
    search_word = request.GET.get("search_word")
    if search_word:
        sql = "SELECT * FROM blog_blog WHERE blog_content LIKE '%%" + search_word + "%%' or blog_title LIKE '%%" + search_word + "%%'"
        blog_list = Blog.objects.raw(sql)
        context = {'blog_list': blog_list, 'page': 'false'}
        return render(request, 'blog/index.html', context)

    #归档分类
    classify = request.GET.get("classify")
    if classify:
        sql = "SELECT * FROM blog_blog WHERE blog_type LIKE '%%" + classify + "%%'"
        blog_list = Blog.objects.raw(sql)
        context = {'blog_list': blog_list, 'page': 'false'}
        return render(request, 'blog/index.html', context)

    context = {'blog_list': blog_list, 'page_no': page_no, 'is_last_page': is_last_page, 'latest_blog_title_list': latest_blog_title_list,
               'classify_dict': classify_dict, 'page':'true'}
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
    blog = Blog.objects.get(blog_title = title)  #get方法返回单个blog
    #每次查询阅读次数加1
    Blog(id=blog.id, blog_title=blog.blog_title, blog_content=blog.blog_content, update_time=blog.update_time,
            modify_time=blog.modify_time, blog_tag=blog.blog_tag, blog_type=blog.blog_type, music = blog.music,
            reading_count=blog.reading_count + 1).save()
    comment_list = Comment.objects.filter(blog_id = blog.id).order_by('-comment_time')
    sub_comment_list = []
    for comment in comment_list:
        sub_comment_list += SubComment.objects.filter(comment_id = comment.id).order_by('-comment_time')
    context = {'blog': blog, 'comment_list': comment_list, 'sub_comment_list': sub_comment_list}
    return render(request, 'blog/detail.html', context)


#新建、更新博客
@csrf_exempt
@login_required
def publish(request):
    if request.method == 'POST':
        md_name_list_str = request.POST.get('md_name_list')
        md_name_list = md_name_list_str.split(',')
        blog_list = Blog.objects.order_by('-update_time')
        blog_title_list = [blog.blog_title for blog in blog_list]
        for md_name in md_name_list:
            file_path = os.path.join(BASE_DIR, 'static/markdowns/' + md_name + '.md')
            blog_dict = parser(file_path)
            title = blog_dict['title'] #str转为unicode
            if len(title.strip()) == 0: #如果标题去除左右空格后长度为零
                return JsonResponse({'status': 'error'})
            if title in blog_title_list:
                blog = Blog.objects.get(blog_title=title)
                blog_id = blog.id
                update_time = blog.update_time
                reading_count = blog.reading_count
            else:
                blog_id = None
                update_time = timezone.now()
                reading_count = 1  #默认阅读次数为1
            classify = blog_dict['classify']
            keywords = blog_dict['keywords']
            content = blog_dict['content']
            music = blog_dict['music']
            blog = Blog(id=blog_id, blog_title=title, blog_content=content, update_time=update_time,
                        modify_time=timezone.now(), blog_tag=keywords, blog_type=classify, reading_count=reading_count, music=music)
            blog.save()
        return JsonResponse({'status': 'success'})
    if request.method == 'GET':
        #return render(request, 'blog/markdown.html')
        return render(request, 'blog/publish.html')

#返回所有的md文件名
@csrf_exempt
@login_required
def get_md_info(request):
    md_path = os.path.join(BASE_DIR, 'static/markdowns')
    md_list = os.listdir(md_path)
    #按时间先后顺序排列
    md_list.sort(key=lambda md: os.stat(os.path.join(md_path, md)).st_mtime, reverse=True)
    md_info_dict = {}  # 存储所有的markdown文件名，转为json对象时使用
    md_info_list = []  # 存储md文件信息列表
    for md in md_list:
        md_info = {}  # 存储单个md信息
        if 'Windows' in platform.system(): #Windows平台，os.listdir()采用gbk编码
            md_info.setdefault('mdName', md[:len(md)-3].decode('gbk').encode('utf-8')) #去掉'md'后缀
        else:  #其它平台
            md_info.setdefault('mdName', md[:len(md) - 3])  # 去掉'md'后缀
        md_info_list.append(md_info)
    md_info_dict.setdefault('md', md_info_list)
    return JsonResponse(md_info_dict, safe=False)


@csrf_exempt
@login_required
def delete(request):
    if request.method == "POST":
        blog_titles = request.POST.get('title_list')
        if blog_titles:
            blog_title_list = blog_titles.split(',')
            for title in blog_title_list:
                blog_list = Blog.objects.filter(blog_title=title)
                for blog in blog_list:
                    blog.delete()
            return JsonResponse({'status': 'OK'})
    if request.method == "GET":
        return render(request, 'blog/delete.html')

#返回所有的博客标题
@login_required
def get_all_title_info(request):
    blog_list = Blog.objects.order_by('-update_time')
    #blog_title_list = [blog.blog_title for blog in blog_list]
    title_dict = {}
    title_info_list = []
    for blog in blog_list:
        title_info = {'title': blog.blog_title}
        title_info_list.append(title_info)
    title_dict.setdefault('blog_titles', title_info_list)
    return JsonResponse(title_dict, safe=False)


@csrf_exempt
@login_required
def upload(request):
    if request.method == "POST":
        md = request.FILES.get('md')
        if md:
            mdFile = open(os.path.join(BASE_DIR, 'static/markdowns/' + md.name), 'wb+')
            mdFile.write(md.read())
            mdFile.close()
    return render(request, 'blog/upload.html')

def comment(request):  #一级评论
    nickname = request.POST.get("nickname")
    content = request.POST.get("content")
    email = request.POST.get("email")
    blog_id = request.POST.get("blog_id")
    comment_time = timezone.now()
    comment = Comment(nickname=nickname, blog_id=blog_id, content= content, comment_time=comment_time, email=email)
    comment.save()
    return JsonResponse({'status':'OK'})

def search_blog(request):
    search_word = request.GET.get("search_word")
    sql = "SELECT * FROM blog_blog WHERE blog_content LIKE '%%" + search_word + "%%' or blog_title LIKE '%%" + search_word + "%%'"
    blog_list = Blog.objects.raw(sql)
    context = {'blog_list': blog_list}
    return render(request, 'blog/index.html', context)

def sub_comment(request): #二级评论
    nickname = request.POST.get("nickname")
    parent_comment_id = request.POST.get("parent_comment_id")
    sub_comment_content = request.POST.get("sub_comment_content")
    email = request.POST.get("email")
    comment_time = timezone.now()
    comment = SubComment(nickname=nickname, comment_id=parent_comment_id, content=sub_comment_content, comment_time=comment_time, email=email)
    comment.save()
    return JsonResponse({'status': 'OK'})

def about(request):  #关于我页面
    return render(request, 'blog/about.html')

def archive(request): #归档
    blog_list = Blog.objects.order_by('-update_time')
    context = {'blog_list': blog_list}
    return render(request, 'blog/archive.html', context)

@login_required
def myadmin(request):
    return render(request, 'blog/myadmin.html')

@login_required
def documents(request):
    filename = request.GET.get('title')
    if filename:
        #file_path = os.path.join(os.getcwd(), "blog", "static", "markdowns", filename + ".md") #开发环境
        file_path = os.path.join("/home/github/django_blog/blog" , "static" , "markdowns",  filename + ".md") #apache环境
        file = open(file_path).read()
        response = StreamingHttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename.encode('utf-8') + ".md")
        return response
    else:
        return render(request, "blog/documents.html")













