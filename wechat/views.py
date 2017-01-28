#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import hashlib
import sign
from django.utils import timezone
from .models import Location
import time
import os
import urllib, urllib2,json
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'wechat/index.html')

def verification(request):
    if request.method == 'GET':
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        # 自己的token
        token = "yaphone"  # 这里改写你在微信公众平台里输入的token
        # 字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        # sha1加密算法
        #print signature, timestamp, nonce, echostr

        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            print "OK"
            return HttpResponse(echostr, content_type="text/plain")

def wechatjs(request): #微信JS验证文件
    return render(request, 'wechat/MP_verify_w1ExVKCAt7pVaCbt.txt')

def my_sign(request): #生成签名随机串
    #file = open("/home/github/django_blog/wechat/util/ticket.txt")
    #jsapi_ticket = file.read()[:-1]  #.read()方法会在字符串后加一个换行符，这里去掉
    #jsapi_ticket = 'kgt8ON7yVITDhtdwci0qeTWQwsqkmCCxl3Cird9AlCT5uvbeLnCEawfiV9IBANNlE6pgrZEIqEVWR3O69OEGhQ'
    #url = "http://zhouyafeng.cn/wechat/"
    #S = sign.Sign(jsapi_ticket, url)
    #ret = S.sign()
    ret = {}
    return JsonResponse(ret)

def save_location(request):
    if request.method == "GET":
        latitude = request.GET.get('latitude') #纬度
        longitude = request.GET.get('longitude') #经度
        ip = request.GET.get('ip') #用户IP地址
        print latitude
        time = timezone.now()
        location = Location(latitude=latitude, longitude=longitude, time=time, ip=ip)
        location.save()
        return JsonResponse({"status": "OK"})


@login_required
def show_location(request):
    if request.method == "GET":
        locations = Location.objects.order_by('-time')
        context = {'locations': locations}
        return render(request, 'wechat/show_location.html', context)
    return render(request, 'wechat/show_location.html')

def show_map(request):
    id = request.GET.get("id")
    context = {"id": id}
    return render(request, 'wechat/show_map.html', context)

def get_specific_location(request):
    id = request.GET.get("id")
    location = Location.objects.get(id=id)
    latitude = location.latitude
    longitude = location.longitude
    return JsonResponse({"longitude": longitude, "latitude": latitude})

def news(request):
    return render(request, "wechat/news.html")

def get_news(request):
    json_res = urllib.urlopen(
        "http://op.juhe.cn/onebox/news/query?key=2a0030ef30ad3c7c65173371aa490a1e&q=%E6%99%AE%E4%BA%AC")
    res = json.load(json_res)
    return JsonResponse(res)

