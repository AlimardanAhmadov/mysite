"""Integrate with admin module."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
#from django.utils.translation import ugettext_lazy as _

# for Django v4
from django.utils.translation import gettext_lazy as _

from .models import User, Products, Orders

admin.site.register(Products)
admin.site.register(Orders)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'parasut_client_id','woocommerce_api_secret')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff','parasut_client_id','woocommerce_api_secret')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
