# -*- coding: utf-8 -*-
# Create your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class SclMUser(models.Model):
    open_id = models.CharField(max_length=50, blank=False, verbose_name='OpenId')
    user_phone = models.CharField(max_length=20, blank=False, verbose_name=u'手机号')
    customerclass = models.CharField(max_length=20, blank=False, verbose_name=u'入口平台')

    def __unicode__(self):
        return self.user_phone

