# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-26 11:59
from __future__ import unicode_literals

from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_video'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='folder',
            options={'ordering': ('name',), 'permissions': (('can_use_directory_listing', 'Can use directory listing'),), 'verbose_name': 'Folder', 'verbose_name_plural': '\u77e5\u8bc6\u5e93'},
        ),
        migrations.AlterField(
            model_name='folder',
            name='diricon',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='img/', verbose_name='\u76ee\u5f55\u56fe\u6807'),
        ),
    ]
