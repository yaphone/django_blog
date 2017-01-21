from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^auth$', views.auth, name='auth'),
    url(r'^user_logout$', views.user_logout, name='user_logout'),
    url(r'^detail$', views.detail, name='detail'),
    url(r'^publish$', views.publish, name="publish"),
    url(r'^get_md_info$', views.get_md_info, name="get_md_info"),
    url(r'^delete$', views.delete, name='delete'),
    url(r'^get_all_title_info$', views.get_all_title_info, name='get_all_title_info'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^comment$', views.comment, name='comment'),
    url(r'^search_blog', views.search_blog, name='search_blog'),
    url(r'^sub_comment', views.sub_comment, name='sub_comment'),
    url(r'^about', views.about, name="about"),
    url(r'^archive', views.archive, name="archive"),
    url(r'^myadmin', views.myadmin, name="myadmin"),
    url(r'^documents', views.documents, name="documents"),

]