#coding=utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Location(models.Model):
    latitude = models.CharField(max_length=100)  # 纬度
    longitude = models.CharField(max_length=100)  # 经度
    time = models.DateTimeField() #时间
    ip = models.CharField(max_length = 100)