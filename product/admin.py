from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Product, ProductImage, ProductVariant,
    Attribute, AttributeValue, Review, Coupon, Discount
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug', 'product_count')
    list_filter = ('parent',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'price', 'current_price_display', 'in_stock', 'is_active_display')
    list_filter = ('category', 'user', 'in_stock')
    search_fields = ('title', 'slug', 'description', 'user__email')
    readonly_fields = ('slug', 'current_price_display', 'created_at_display', 'updated_at_display')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'slug', 'category')
        }),
        ('Pricing', {
            'fields': ('price', 'buy_price', 'current_price_display')
        }),
        ('Inventory', {
            'fields': ('in_stock',)
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at_display', 'updated_at_display'),
            'classes': ('collapse',)
        }),
    )

    def current_price_display(self, obj):
        price = obj.current_price
        if price < obj.price:
            return format_html('<span style="color: #22c55e;">${:.2f}</span> (was ${:.2f})', price, obj.price)
        return f'${price:.2f}'
    current_price_display.short_description = 'Current Price'

    def is_active_display(self, obj):
        return obj.in_stock is not None and obj.in_stock > 0
    is_active_display.boolean = True
    is_active_display.short_description = 'In Stock'

    def created_at_display(self, obj):
        from django.utils import timezone
        return obj.created_at.strftime('%Y-%m-%d %H:%M') if hasattr(obj, 'created_at') else '-'
    created_at_display.short_description = 'Created'

    def updated_at_display(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M') if hasattr(obj, 'updated_at') else '-'
    updated_at_display.short_description = 'Updated'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px;"/>', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'product', 'attributes_list')
    search_fields = ('product__title',)
    filter_horizontal = ('attributes',)

    def attributes_list(self, obj):
        return ', '.join([str(attr) for attr in obj.attributes.all()])
    attributes_list.short_description = 'Attributes'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image_preview', 'uploaded_at')
    search_fields = ('product__title',)
    readonly_fields = ('image_preview', 'uploaded_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px;"/>', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'

    def uploaded_at(self, obj):
        return obj.product.created_at.strftime('%Y-%m-%d') if obj.product.created_at else '-'
    uploaded_at.short_description = 'Uploaded'


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'value_count')
    search_fields = ('name',)
    ordering = ('name',)

    def value_count(self, obj):
        return obj.values.count()
    value_count.short_description = 'Values'


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('value', 'attribute')
    list_filter = ('attribute',)
    search_fields = ('value', 'attribute__name')
    ordering = ('attribute__name', 'value')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'stars_display', 'created_at')
    list_filter = ('stars', 'created_at')
    search_fields = ('product__title', 'user__email', 'review')
    readonly_fields = ('created_at',)

    def stars_display(self, obj):
        return '★' * obj.stars + '☆' * (5 - obj.stars)
    stars_display.short_description = 'Rating'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'product', 'value', 'start_date', 'end_date', 'is_active')
    list_filter = ('end_date',)
    search_fields = ('code', 'product__title')
    readonly_fields = ('start_date',)

    def is_active(self, obj):
        from django.utils import timezone
        return obj.end_date > timezone.now()
    is_active.boolean = True
    is_active.short_description = 'Active'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('product', 'discounted_price', 'percentage_display', 'start_date', 'end_date', 'is_active')
    list_filter = ('end_date',)
    search_fields = ('product__title',)
    readonly_fields = ('start_date',)

    def percentage_display(self, obj):
        if obj.product and obj.product.price > 0:
            pct = ((obj.product.price - obj.discounted_price) / obj.product.price) * 100
            return f'{pct:.1f}%'
        return '-'
    percentage_display.short_description = 'Discount %'

    def is_active(self, obj):
        from django.utils import timezone
        return obj.end_date > timezone.now()
    is_active.boolean = True
    is_active.short_description = 'Active'


# ProductAdmin with inlines is already registered via @admin.register(Product) above