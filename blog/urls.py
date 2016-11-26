from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^publish$', views.publish, name='publish'),
    url(r'^publish_article$', views.publish_article, name='publish_article'),
    url(r'^auth', views.auth, name='auth'),
    url(r'^user_logout', views.user_logout, name='user_logout'),
    url(r'^detail', views.detail, name='detail'),
    url(r'^get_markdowns', views.get_markdowns, name='get_markdowns'),
]