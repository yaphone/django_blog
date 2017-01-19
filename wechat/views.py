#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import hashlib
import sign
from django.utils import timezone
from.models import Location
import time
import os
import urllib2,json
import json


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
    jsapi_ticket = 'kgt8ON7yVITDhtdwci0qeTWQwsqkmCCxl3Cird9AlCRmtrhZBZHyDl7X_IhVYAchSqwhe5yDWtPUTx7oJpJ0WQ'
    #pre_url = "zhouyafeng.cn/wechat"
    url = "http://zhouyafeng.cn/wechat/"
    S = sign.Sign(jsapi_ticket, url)
    ret = S.sign()
    return JsonResponse(ret)

def save_location(request):
    if request.method == "GET":
        latitude = request.GET.get('latitude') #纬度
        longitude = request.GET.get('longitude') #经度
        time = timezone.now()
        location = Location(latitude=latitude, longitude=longitude, time=time)
        location.save()
        return JsonResponse({"status": "OK"})

def show_location(request):
    if request.method == "GET":
        sql = "SELECT * FROM wechat_location"
        locations = Location.objects.raw(sql)
        context = {'locations': locations}
        return render(request, 'wechat/show_location.html', context)
    return render(request, 'wechat/show_location.html')

def show_map(request):
    id = request.GET.get("id")
    location = Location.objects.get(id=id)
    context = {"location": location}
    return render(request, 'wechat/show_map.html', context)
