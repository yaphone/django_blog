from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^verification$', views.verification, name='verification'),
    url(r'^MP_verify_w1ExVKCAt7pVaCbt.txt$', views.wechatjs, name='verification'),
    url(r'^sign$', views.my_sign, name="sign"),

]