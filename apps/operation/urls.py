from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^(?P<folder_id>\d+)/$',views.directory_listing,name='directory_listing'),
    # url(r'^(?P<folder_name>[\w\-]+)/$',views.directory_listing,name='directory_listing'),
]
