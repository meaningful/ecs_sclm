# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models

# Create your models here.

import logging
import os
from distutils.version import LooseVersion

from django import get_version
from django.db import models
from django.utils.translation import ugettext_lazy as _
import logging
import os

from filer import settings as filer_settings
from filer.models.filemodels import File

logger = logging.getLogger(__name__)

DJANGO_GTE_17 = LooseVersion(get_version()) >= LooseVersion('1.7.0')

class Video(File):

    file_type = 'Video'
    _icon = "video"
    videourl = models.URLField(verbose_name=(u'视频地址'), blank=True, null=True)
    # default_alt_text = models.CharField(_(u'视频不存在'), max_length=255, blank=True, null=True)
    @classmethod
    def matches_file_type(cls, iname, ifile, request):
        # This was originally in admin/clipboardadmin.py  it was inside of a try
        # except, I have moved it here outside of a try except because I can't
        # figure out just what kind of exception this could generate... all it was
        # doing for me was obscuring errors...
        # --Dave Butler <croepha@gmail.com>
        iext = os.path.splitext(iname)[1].lower()
        return iext in ['.mp4', '.avi', '.gif']

    # def save(self, *args, **kwargs):
    #     # self.has_all_mandatory_data = self._check_validity()
    #     super(Video, self).save(*args, **kwargs)

    # def _check_validity(self):
    #     # if not self.name:
    #     #     return False
    #     return True

    # def has_edit_permission(self, request):
    #     return self.has_generic_permission(request, 'edit')

    # def has_read_permission(self, request):
    #     return self.has_generic_permission(request, 'read')

    # # def has_add_children_permission(self, request):
    # #     return self.has_generic_permission(request, 'add_children')

    # def has_generic_permission(self, request, permission_type):
    #     """
    #     Return true if the current user has permission on this
    #     image. Return the string 'ALL' if the user has all rights.
    #     """
    #     user = request.user
    #     if not user.is_authenticated():
    #         return False
    #     elif user.is_superuser:
    #         return True
    #     elif user == self.owner:
    #         return True
    #     # elif self.folder:
    #         # return self.folder.has_generic_permission(request, permission_type)
    #     else:
    #         return False

    @property
    def label(self):
        if self.name in ['', None]:
            return self.original_filename or 'unnamed file'
        else:
            return self.name

    class Meta(object):
        app_label = 'filer'
        verbose_name = _(u'视频')
        verbose_name_plural = _('视频')
filer_settings.FILER_FILE_MODELS = (Video,) + filer_settings.FILER_FILE_MODELS
# abstract = True
