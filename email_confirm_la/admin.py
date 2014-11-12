# coding: utf-8

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from email_confirm_la.models import EmailConfirmation


class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'content_object', 'email_field_name', 'email', 'is_verified', 'is_primary', 'send_at', 'confirmed_at')
    list_display_links = list_display
    search_fields = ('email', )
    ordering = ('-id', )

admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
