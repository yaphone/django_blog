from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^publish$', views.publish, name='publish'),
    url(r'^publish_article$', views.publish_article, name='publish_article'),
    url(r'^auth$', views.auth, name='auth'),
    url(r'^user_logout$', views.user_logout, name='user_logout'),
    url(r'^detail$', views.detail, name='detail'),
#    url(r'^get_markdowns', views.get_markdowns, name='get_markdowns'),
    url(r'^markdowns$', views.markdowns, name="markdowns"),
    url(r'^get_md_info$', views.get_md_info, name="get_md_info"),
    url(r'^get_md_name_list$', views.get_md_name_list, name="get_md_name_list"),
    url(r'^delete_page$', views.delete_page, name='delete_page'),
    url(r'^get_all_title_info$', views.get_all_title_info, name='get_all_title_info'),
    url(r'^delete_select_blog$', views.delete_select_blog, name='delete_select_blog'),
    url(r'^upload$', views.upload, name='upload'),

]