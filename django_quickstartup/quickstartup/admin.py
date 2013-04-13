# coding: utf-8


from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import PageForm, CustomUserChangeForm, CustomUserCreationForm
from .models import Page, User, Contact


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


class UserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ("email", "is_staff", "last_login")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")},),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ('groups', 'user_permissions')


if get_user_model() is User:
    admin.site.register(User, UserAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('updated_at', 'name', 'email', 'phone', 'status')
    list_display_links = ('updated_at', 'name', 'email', 'phone')
    list_editable = ("status",)
    list_filter = ('status',)
    search_fields = ('name', 'email')
    ordering = ("-updated_at",)


admin.site.register(Contact, ContactAdmin)