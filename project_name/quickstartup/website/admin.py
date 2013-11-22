# coding: utf-8


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .forms import PageForm
from .models import Page, Contact


class PageAdmin(admin.ModelAdmin):
    form = PageForm
    fieldsets = (
        (None, {'fields': ('name', 'url', 'title', 'content')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('registration_required', 'template_name')}),
    )
    list_display = ('name', 'url', 'title')
    list_display_links = ('name', 'url', 'title')
    list_filter = ('registration_required',)
    search_fields = ('name', 'url', 'title')


admin.site.register(Page, PageAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('updated_at', 'name', 'email', 'phone', 'status')
    list_display_links = ('updated_at', 'name', 'email', 'phone')
    list_editable = ("status",)
    list_filter = ('status',)
    search_fields = ('name', 'email')
    ordering = ("-updated_at",)


admin.site.register(Contact, ContactAdmin)