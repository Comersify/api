from django.contrib import admin
from django.utils.html import format_html
from .models import Tracker, Visit


@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    list_display = ('id_short', 'user', 'created_at', 'visit_count')
    list_filter = ('created_at',)
    search_fields = ('id', 'user__email')
    readonly_fields = ('id', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def id_short(self, obj):
        return str(obj.id)[:8] + '...'
    id_short.short_description = 'Tracker ID'

    def visit_count(self, obj):
        return obj.visit_set.count()
    visit_count.short_description = 'Visits'


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('tracker_short', 'client_url', 'browser', 'ip_address', 'logged_in_display', 'timestamp')
    list_filter = ('browser', 'logged_in', 'sub_domain')
    search_fields = ('tracker__id', 'client_url', 'client_path', 'ip_address')
    readonly_fields = ('tracker', 'client_url', 'client_path', 'api_path', 'browser', 'sub_domain', 'ip_address', 'logged_in', 'timestamp')

    def tracker_short(self, obj):
        return str(obj.tracker.id)[:8] + '...'
    tracker_short.short_description = 'Tracker'

    def logged_in_display(self, obj):
        return obj.logged_in
    logged_in_display.boolean = True
    logged_in_display.short_description = 'Logged In'

    def timestamp(self, obj):
        from django.utils import timezone
        return obj.tracker.created_at.strftime('%Y-%m-%d %H:%M') if obj.tracker.created_at else '-'
    timestamp.short_description = 'Time'
