"""sclmknowledge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import view
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^$',view.index),
    url(r'^admin/prodire/', include('prodire.urls')),
    # url(r'^admin/prodire/updatePicture/$', prodire.views.updatePicture),
    url(r'^admin/', admin.site.urls),
    url(r'^filer/', include('filer.urls')),
    url(r'^operation/', include('operation.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
