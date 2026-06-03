from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser, ShippingInfo, Store, AppReviews, Token


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'user_type', 'is_active', 'is_staff', 'created_at')
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        ('Personal Info', {
            'fields': ('email', 'username', ('first_name', 'last_name'), 'phone_number', 'image')
        }),
        ('User Type', {
            'fields': ('user_type',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
    )

    def created_at(self, obj):
        return obj.date_joined.strftime('%Y-%m-%d')
    created_at.short_description = 'Created'


@admin.register(ShippingInfo)
class ShippingInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number', 'postal_code')
    search_fields = ('user__email', 'address', 'phone_number', 'postal_code')
    list_filter = ('postal_code',)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'logo_preview')
    search_fields = ('name', 'user__email', 'description')
    readonly_fields = ('logo_preview', 'cover_preview')

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.cover.url)
        return '-'
    cover_preview.short_description = 'Cover'


@admin.register(AppReviews)
class AppReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'stars_display', 'created_at', 'short_review')
    list_filter = ('stars', 'created_at')
    search_fields = ('user__email', 'review')
    readonly_fields = ('created_at',)

    def stars_display(self, obj):
        return '★' * obj.stars + '☆' * (5 - obj.stars)
    stars_display.short_description = 'Rating'

    def short_review(self, obj):
        return obj.review[:50] + '...' if len(obj.review) > 50 else obj.review
    short_review.short_description = 'Review'


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token_preview', 'created')
    search_fields = ('user__email', 'token')
    readonly_fields = ('token',)

    def token_preview(self, obj):
        return obj.token[:20] + '...'
    token_preview.short_description = 'Token'

    def created(self, obj):
        return obj.user.date_joined.strftime('%Y-%m-%d')
    created.short_description = 'Created'

# Custom Admin Site for email-based authentication
from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    login_template = 'admin/login.html'
    
    def login(self, request, extra_context=None):
        # Handle email-based login
        from django.contrib.auth import authenticate, login
        if request.method == 'POST':
            email = request.POST.get('username')  # username field contains email
            password = request.POST.get('password')
            from user.models import CustomUser
            try:
                user = CustomUser.objects.get(email=email)
                if user.check_password(password):
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    return HttpResponseRedirect(request.POST.get('next', '/admin/'))
            except CustomUser.DoesNotExist:
                pass
        return super().login(request, extra_context)

admin_site = CustomAdminSite(name='admin')
