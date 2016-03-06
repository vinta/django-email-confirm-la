# coding: utf-8

from django.contrib import admin

from email_confirm_la.models import EmailConfirmation


def resend_confirmation_email(modeladmin, request, queryset):
    for confirmation in queryset:
            confirmation.send()

resend_confirmation_email.short_description = 'Re-send selected %(verbose_name_plural)s'


class EmailConfirmationAdmin(admin.ModelAdmin):

    def show_content_type(self, obj):
        if not obj.content_object:
            return None
        return obj.content_object._meta.object_name
    show_content_type.short_description = 'Content type'

    actions = [resend_confirmation_email, ]
    list_display = ('show_content_type', 'content_object', 'email_field_name', 'email', 'send_at')
    list_display_links = list_display
    search_fields = ('email', )
    ordering = ('-id', )

admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
