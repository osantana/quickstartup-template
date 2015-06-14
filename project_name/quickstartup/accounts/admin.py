# coding: utf-8


from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import User


class UserAdmin(DjangoUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ("name", "email", "is_staff", "last_login")
    list_filter = ("is_staff", "is_active", "groups")
    fieldsets = (
        (None, {"fields": ("name", "email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("name", "email", "password1", "password2", "is_staff"),
        },),
    )
    search_fields = ("name", "email")
    ordering = ("name", "email")
    filter_horizontal = ('groups', 'user_permissions')


# Enable admin interface if User is the quickstart user model
if get_user_model() is User:
    admin.site.register(User, UserAdmin)
