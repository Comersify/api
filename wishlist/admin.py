from django.contrib import admin
from django.utils.html import format_html
from .models import WishList


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_count', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__email',)
    readonly_fields = ('created_at',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'

    def created_at(self, obj):
        return obj.id
    created_at.short_description = 'Created'
