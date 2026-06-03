from django.contrib import admin
from django.utils.html import format_html
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'status_display', 'price_display', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'product__title', 'id')
    readonly_fields = ('price', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Order Details', {
            'fields': ('user', 'product', 'quantity')
        }),
        ('Status & Pricing', {
            'fields': ('status', 'coupon', 'price', 'shipping')
        }),
        ('Shipping', {
            'fields': ('shipping_info',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def status_display(self, obj):
        colors = {
            'IN_CART': '#f59e0b',
            'SUBMITTED': '#0ea5e9',
            'SHIPPED': '#8b5cf6',
            'DELEVRED': '#22c55e',
        }
        color = colors.get(obj.status, '#71717a')
        return format_html(
            '<span style="background: {}; color: white; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.75rem; font-weight: 600;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'

    def price_display(self, obj):
        if obj.price:
            return f'${obj.price:.2f}'
        return '-'
    price_display.short_description = 'Price'
