from django.contrib import admin
from django.utils.html import format_html
from .models import Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain', 'test_domain', 'user', 'logo_preview')
    list_filter = ('user',)
    search_fields = ('title', 'domain', 'test_domain', 'user__email')
    readonly_fields = ('logo_preview_large',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 40px;"/>', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'

    def logo_preview_large(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 150px;"/>', obj.logo.url)
        return '-'
    logo_preview_large.short_description = 'Logo Preview'
