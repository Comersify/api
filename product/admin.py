from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductPackage)
admin.site.register(Review)
admin.site.register(Coupon)
admin.site.register(Discount)
