# -*- coding: utf-8 -*-

"""Admin classes for data models."""

from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from djpagan.tuition.models import GenericChoice
from djpagan.tuition.models import Remission


class GenericChoiceAdmin(admin.ModelAdmin):
    """GenericChoice admin class."""

    list_display = ('name', 'value', 'ranking', 'active')
    list_editable = ('active',)
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class RemissionAdmin(admin.ModelAdmin):
    """Remission admin class."""

    list_display = [
        'user_last_name',
        'user_first_name',
        'user_email',
        'username',
        'cid',
        'income',
        'created_at',
        'percentage',
        'approved',
    ]
    list_editable = ('approved', 'percentage')
    ordering = ['user__last_name', 'user__first_name']
    search_fields = (
        'user__last_name',
        'user__first_name',
        'user__email',
        'user__username',
        'user__id',
    )
    date_hierarchy = 'created_at'
    list_per_page = 500
    raw_id_fields = ('user', 'updated_by')

    def user_last_name(self, instance):
        """Return the user's last name."""
        return instance.user.last_name

    def user_first_name(self, instance):
        """Return the user's first name."""
        return instance.user.first_name

    def user_email(self, instance):
        """Return the user's email."""
        return instance.user.email

    def cid(self, instance):
        """Return the user's ID."""
        return instance.user.id

    def username(self, instance):
        """Return the user's username."""
        return instance.user.username


admin.site.register(GenericChoice, GenericChoiceAdmin)
admin.site.register(Remission, RemissionAdmin)
