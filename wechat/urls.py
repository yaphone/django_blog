#coding=utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^verification$', views.verification, name='verification'),
    url(r'^MP_verify_w1ExVKCAt7pVaCbt.txt$', views.wechatjs, name='verification'),
    url(r'^sign$', views.my_sign, name="sign"),
    url(r'^save_location$', views.save_location, name="save_location"),
    url(r'^show_location$', views.show_location, name="show_location"),
    url(r'^show_map$', views.show_map, name="show_map"),
    url(r'^get_specific_location$', views.get_specific_location, name="get_specific_location"),
    url(r'^news$', views.news, name="news"),
    url(r'^get_news$', views.get_news, name="get_news"),



]