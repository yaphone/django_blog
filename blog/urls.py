from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^auth$', views.auth, name='auth'),
    url(r'^user_logout$', views.user_logout, name='user_logout'),
    url(r'^detail$', views.detail, name='detail'),
    url(r'^markdowns$', views.markdowns, name="markdowns"),
    url(r'^get_md_info$', views.get_md_info, name="get_md_info"),
    url(r'^delete$', views.delete, name='delete'),
    url(r'^get_all_title_info$', views.get_all_title_info, name='get_all_title_info'),
    url(r'^upload$', views.upload, name='upload'),

]