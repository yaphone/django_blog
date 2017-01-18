#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
import hashlib
import time
import os
import urllib2,json
import json

# Create your views here.

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'wechat/test.html')

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
        
