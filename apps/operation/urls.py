from django.conf.urls import url

from . import views

from .views import WeChat
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^indexzm', views.indexzm, name='indexzm'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^(?P<folder_id>\d+)/$',views.directory_listing,name='directory_listing'),
    # url(r'^wx_index/$', views.wx_index, name='wx_index'),
    url(r'^phone_bind/$', views.phone_bind, name='phone_bind'),
    url(r'^send_msg/$', views.send_msg, name='send_msg'),
    # url(r'^(?P<folder_name>[\w\-]+)/$',views.directory_listing,name='directory_listing'),
    url(r'^wechat/$', WeChat.as_view()),
    url(r'^get_openid', views.index, name='get_openid'),
    url(r'^go_search/$', views.go_search, name='go_search'),
    url(r'^search/$', views.search, name='search')
]
