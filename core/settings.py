from datetime import timedelta
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = int(os.environ.get("ENV", 0) == "DEV")

ALLOWED_HOSTS = ["*"]


AUTH_USER_MODEL = 'user.CustomUser'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
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
    'website'
]

# If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
# CORS_ORIGIN_ALLOW_ALL = True
DATA_UPLOAD_MAX_MEMORY_SIZE = None
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_REGEX_WHITELIST = [
    r"^http://\w+\.localhost:3000",
    r"^https://\w+\.comercify.shop",
    r"^http://\w+\.comercify.shop",
]

CORS_ALLOWED_ORIGINS = [
    "https://api.comercify.shop",
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3005',
    "https://comercify-dashboard.vercel.app",
    "https://comercify.vercel.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://api.comercify.shop",
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3005',
    "https://comercify-dashboard.vercel.app",
    "https://comercify.vercel.app",
]

CORS_ALLOW_HEADERS = [
    "X-Comercify-Visitor",
    "X-Comercify-Owner",
    "Authorization",
    "Content-Type",
]

CORS_ALLOWED_METHODS = [
    'GET', 'POST', 'DELETE', 'PUT'
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
    'tracking.middleware.TrackerMiddleware',
    'tracking.middleware.SubDomainMiddleware',
]

if not DEBUG:
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'core.middleware.TokenToUserMiddleware',
        'tracking.middleware.TrackerMiddleware',
        'tracking.middleware.SubDomainMiddleware',
    ]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

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


WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("PGDATABASE"),
        'HOST': os.environ.get("PGHOST"),
        'PASSWORD': os.environ.get("PGPASSWORD"),
        'PORT': os.environ.get("PGPORT"),
        'USER': os.environ.get("PGUSER"),
    }
}


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


""" 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_SERVER')
EMAIL_HOST_USER = os.getenv('EMAIL_USERNAME')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = True 
"""

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,

    # this is the maximum time AFTER the token was issued that
    # it can be refreshed.  exprired tokens can't be refreshed.
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, '/static/staticfiles')
STATIC_URL = '/static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    '/var/www/static/'
]