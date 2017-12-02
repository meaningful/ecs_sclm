# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from .. import settings
from ..models import File,FilePermission
from ..utils.compatibility import LTE_DJANGO_1_5, LTE_DJANGO_1_6, unquote
from .permissions import PrimitivePermissionAwareModelAdmin
from .tools import AdminContext, admin_url_params_encoded, popup_status

from django.forms import CheckboxSelectMultiple
from django.db.models import Q
from django.contrib.auth.models import Group, Permission, User
# class FilerPermissionInline(admin.TabularInline):
#     model = FilePermission

# class FilePermissionInline(admin.StackedInline):
#     model = FilePermission

class FileAdminChangeFrom(forms.ModelForm):
    
    class Meta(object):
        model = File
        exclude = ()


class FileAdmin(PrimitivePermissionAwareModelAdmin):
    list_display = ('label',)
    list_per_page = 10
    search_fields = ['name', 'original_filename', 'sha1', 'description']
    raw_id_fields = ('owner', )
    readonly_fields = ('sha1', 'display_canonical')
    inlines = [
        # FilePermissionInline,
    ]
    
    # save_as hack, because without save_as it is impossible to hide the
    # save_and_add_another if save_as is False. To show only save_and_continue
    # and save in the submit row we need save_as=True and in
    # render_change_form() override add and change to False.
    save_as = True

    form = FileAdminChangeFrom

    def get_queryset(self, request):
        if LTE_DJANGO_1_5:
            return super(FileAdmin, self).queryset(request)
        return super(FileAdmin, self).get_queryset(request)

    @classmethod
    def build_fieldsets(cls, extra_main_fields=(), extra_advanced_fields=(),
                        extra_fieldsets=()):
        fieldsets = (
            (None, {
                'fields': (
                    'name',
                    # 'owner',
                    'description',
                ) + extra_main_fields,
            }),
            (_('Advanced'), {
                'fields': (
                    'file',
                    # 'sha1',
                    # 'display_canonical',
                    'ispublic',
                    'perm',
                ) + extra_advanced_fields,
                # 'classes': ('collapse',),
            }),
        # ) + extra_fieldsets
            )
        # if settings.FILER_ENABLE_PERMISSIONS:
        #     fieldsets = fieldsets + (
        #         (None, {
        #             'fields': (
        #                  # 'is_public',
        #                    'ispublic',
        #                    'perm',
        #                    )
        #         }),
        #     )
        return fieldsets

    def response_change(self, request, obj):
        """
        Overrides the default to be able to forward to the directory listing
        instead of the default change_list_view
        """
        if (
            request.POST and
            '_continue' not in request.POST and
            '_saveasnew' not in request.POST and
            '_addanother' not in request.POST
        ):
            # Popup in pick mode or normal mode. In both cases we want to go
            # back to the folder list view after save. And not the useless file
            # list view.
            if obj.folder:
                url = reverse('admin:filer-directory_listing',
                              kwargs={'folder_id': obj.folder.id})
            else:
                url = reverse(
                    'admin:filer-directory_listing-unfiled_images')
            url = "{0}{1}".format(
                url,
                admin_url_params_encoded(request),
            )
            return HttpResponseRedirect(url)
        return super(FileAdmin, self).response_change(request, obj)

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        info = self.model._meta.app_label, self.model._meta.model_name
        extra_context = {'show_delete': True,
                         'history_url': 'admin:%s_%s_history' % info,
                         'is_popup': popup_status(request),
                         'filer_admin_context': AdminContext(request)}
        context.update(extra_context)
        return super(FileAdmin, self).render_change_form(
            request=request, context=context, add=add, change=change,
            form_url=form_url, obj=obj)

    def delete_view(self, request, object_id, extra_context=None):
        """
        Overrides the default to enable redirecting to the directory view after
        deletion of a image.

        we need to fetch the object and find out who the parent is
        before super, because super will delete the object and make it
        impossible to find out the parent folder to redirect to.
        """
        try:
            obj = self.get_queryset(request).get(pk=unquote(object_id))
            parent_folder = obj.folder
        except self.model.DoesNotExist:
            parent_folder = None

        admin_context = AdminContext(request)
        if LTE_DJANGO_1_6:
            extra_context = extra_context or {}
            extra_context.update({'is_popup': admin_context.popup})
        if request.POST:
            # Return to folder listing, since there is no usable file listing.
            super(FileAdmin, self).delete_view(
                request=request, object_id=object_id,
                extra_context=extra_context)
            if parent_folder:
                url = reverse('admin:filer-directory_listing',
                              kwargs={'folder_id': parent_folder.id})
            else:
                url = reverse('admin:filer-directory_listing-unfiled_images')
            url = "{0}{1}".format(
                url,
                admin_url_params_encoded(request)
            )
            return HttpResponseRedirect(url)

        return super(FileAdmin, self).delete_view(
            request=request, object_id=object_id,
            extra_context=extra_context)

    def get_model_perms(self, request):
        """
        It seems this is only used for the list view. NICE :-)
        """
        return {
            'add': False,
            'change': False,
            'delete': False,
        }

    def display_canonical(self, instance):
        canonical = instance.canonical_url
        if canonical:
            return '<a href="%s">%s</a>' % (canonical, canonical)
        else:
            return '-'
    display_canonical.allow_tags = True
    display_canonical.short_description = _('canonical URL')

    #############chenyu change
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if not request.user.is_superuser:  
    #         if db_field.name == "perm":
    #             qs = FilePermission.objects.all()
    #             group_ids = request.user.groups.all().values_list('id', flat=True)
    #             q = Q(groups__in=group_ids) | Q(everybody=True)
    #             kwargs['queryset'] = qs.filter(q).distinct()
    #     return super(FileAdmin,self).formfield_for_foreignkey(db_field, request, **kwargs)        



class FilePermissionAdminChangeFrom(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Group.objects.all())
    # class Meta(object):
    #     model = FilePermission
    #     exclude = ()
    #     widgets = {
    #         'groups': CheckboxSelectMultiple
    #     }

class FilePermissionAdmin(admin.ModelAdmin):
    # list_display = ('name', 'can_read', 'can_edit', 'everybody')
    list_display = ('name', )
    search_fields = ['name']
    form = FilePermissionAdminChangeFrom
    # fields = ('name', 'can_read', 'can_edit', 'everybody', 'groups')
    fields = ('name', 'groups')
    #  chenyu change
    # def get_queryset(self, request):
    #     qs = super(FilePermissionAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     else:
    #         group_ids = request.user.groups.all().values_list('id', flat=True)
    #         q = Q(groups__in=group_ids) | Q(everybody=True)
    #         return qs.filter(q).distinct()
    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if not request.user.is_superuser:  
    #         if db_field.name == "groups":
    #             group_ids = request.user.groups.all().values_list('name', flat=True)
    #             kwargs["queryset"] = group_ids
    #     return super(FilePermissionAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    
FileAdmin.fieldsets = FileAdmin.build_fieldsets()
admin.site.register(FilePermission, FilePermissionAdmin)
