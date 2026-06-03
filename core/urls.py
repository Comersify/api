"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("product.urls")),
    path("", include("order.urls")),
    path("", include("cart.urls")),
    path("", include("wishlist.urls")),
    path("", include("user.urls")),
    path("", include("ads.urls")),
    path("tracking/", include("tracking.urls")),
    path("site/", include("website.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve documentation HTML files from /docs/ path
docs_dir = os.path.join(settings.BASE_DIR, 'templates', 'docs')
if os.path.exists(docs_dir):
    # Serve individual HTML doc pages
    html_files = ['authentication.html', 'products.html', 'cart-orders.html', 'wishlist.html', 'tracking-ads.html']
    for html_file in html_files:
        file_path = os.path.join(docs_dir, html_file)
        if os.path.exists(file_path):
            urlpatterns.append(path(f'docs/{html_file}', TemplateView.as_view(template_name=f'docs/{html_file}')))
    
    # Serve the index
    urlpatterns.append(path('docs/', TemplateView.as_view(template_name='docs/index.html')))
