from django.contrib import admin
from .models import ShoppingCart


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_count', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__email',)
    readonly_fields = ('created_at',)

    def order_count(self, obj):
        return obj.orders.count()
    order_count.short_description = 'Orders'

    def created_at(self, obj):
        return obj.id
    created_at.short_description = 'Created'
