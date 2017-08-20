# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse
from itertools import chain


# Register your models here.
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    readonly_fields = ('content_type', 'user', 'action_time')
    actions = None

    # readonly_fields = LogEntry._meta.get_fields()
    # readonly_fields = list(set(chain.from_iterable(
    #    (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
    #    for field in LogEntry._meta.get_fields()
    # For complete backwards compatibility, you may want to exclude
    # GenericForeignKey from the results.
    #     if not (field.many_to_one and field.related_model is None)
    #        )))

    list_filter = [
        'content_type',
        'action_flag'
    ]

    '''
    search_fields = [
        'object_repr',
        'change_message'
    ]
    '''

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
 #       'change_message',
    ]

    # def get_readonly_fields(self, request, obj=None):
    # return [f.name for f in self.model._meta.get_fields()]
   
   # from itertools import chain
   # list(set(chain.from_iterable(
    #    (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
     #   for field in LogEntry._meta.get_fields()
    # For complete backwards compatibility, you may want to exclude
    # GenericForeignKey from the results.
      #  if not (field.many_to_one and field.related_model is None)
       #     )))
    
    def get_list_display_links(self, request, list_display):

        if self.list_display_links or not list_display:
            return self.list_display_links
        else:
            return


    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
	'''
        if obj.action_flag == DELETION:
           link = escape(obj.object_repr)
        else: 
	   ct = obj.content_type
           link = u'<a href="%s">%s</a>' % (
               reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr)
          )
	'''
        return escape(obj.object_repr)

    def get_list_display_links(self, request, list_display):

        if self.list_display_links or not list_display:
            return self.list_display_links
        else:
            return

    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'内容摘要'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request).prefetch_related('content_type')


admin.site.register(LogEntry, LogEntryAdmin)
