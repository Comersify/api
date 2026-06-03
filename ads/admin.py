from django.contrib import admin
from django.utils.html import format_html
from .models import Ads


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview', 'link', 'is_active', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('link',)
    readonly_fields = ('created_at', 'image_preview_large')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px;"/>', obj.image.url)
        return '-'
    image_preview.short_description = 'Image'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)
        return '-'
    image_preview_large.short_description = 'Preview'

    def is_active(self, obj):
        return obj.end_date is not None
    is_active.boolean = True
    is_active.short_description = 'Active'
