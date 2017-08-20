# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django.contrib import admin

from django import forms

from .models import Video
from filer.admin.fileadmin import FileAdmin

class VideoAdminForm(forms.ModelForm):
    Videourl = forms.URLField(
        label=(u'上传视频地址'),
        help_text=(u'复制视频网站地址')
    )
    class Meta(object):
        model = Video
        exclude = ()


class VideoAdmin(admin.ModelAdmin):
# class VideoAdmin(FileAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'ispublic', 'folder', 'perm', 'owner', 'description', 'videourl')
        }),
    )
    # form = VideoAdminForm


admin.site.register(Video, VideoAdmin) # use the standard FileAdmin

# Register your models here.
