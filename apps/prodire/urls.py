from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'updatePicture', views.updatePicture, name='updatePicture'),
]
