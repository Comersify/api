from datetime import timedelta
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY")


if os.environ.get("ENV") == "DEV":
    DEBUG = True
elif os.environ.get("ENV") == "PROD":
    DEBUG = False


ALLOWED_HOSTS = ["127.0.0.1",".varcel.app"]


AUTH_USER_MODEL = 'user.CustomUser'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'corsheaders',
    'tracking',
    'wishlist',
    'product',
    'order',
    'cart',
    'user',
    'ads',
]

# If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
# CORS_ORIGIN_ALLOW_ALL = True

ADMIN_REACT_SITE = os.environ.get("ADMIN_REACT_SITE")
STORE_NEXT_SITE = os.environ.get("STORE_NEXT_SITE")

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    # ADMIN
    "https://admin-dashboard-pi-woad.vercel.app",
    "https://master--steady-kangaroo-bebaba.netlify.app",

    # Store
    "https://boisterous-clafoutis-4deb4d.netlify.app",
    "https://next-js-ecommerce-hjpfp5hkl-saadaoui-salah.vercel.app",
    ADMIN_REACT_SITE,
    STORE_NEXT_SITE,
]

CSRF_TRUSTED_ORIGINS = [
    # ADMIN
    "https://admin-dashboard-pi-woad.vercel.app",
    "https://master--steady-kangaroo-bebaba.netlify.app",
    ###########
    # STORE
    "https://boisterous-clafoutis-4deb4d.netlify.app",
    "https://next-js-ecommerce-hjpfp5hkl-saadaoui-salah.vercel.app",
    ###########
    ADMIN_REACT_SITE,
    STORE_NEXT_SITE,
]

CORS_ALLOW_CREDENTIALS = True
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.TokenToUserMiddleware',
]

ROOT_URLCONF = 'core.urls'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.app'

DATABASES = {}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'TOKEN_EXPIRED_AFTER': 3600  # Expiry time in seconds (1 hour)
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_SERVER')
EMAIL_HOST_USER = os.getenv('EMAIL_USERNAME')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = True

SIMPLE_JWT = {
    # Expiry time for refresh token (30 days)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
