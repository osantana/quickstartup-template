# coding: utf-8


from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('updated_at', 'name', 'email', 'phone', 'status')
    list_display_links = ('updated_at', 'name', 'email', 'phone')
    list_editable = ("status",)
    list_filter = ('status',)
    search_fields = ('name', 'email')
    ordering = ("-updated_at",)


admin.site.register(Contact, ContactAdmin)
