import os
from pathlib import Path
from decouple import config
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

SECRET_KEY = config("DJANGO_SECRET_KEY", cast=str, default=get_random_secret_key())
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DJANGO_DEBUG", cast=bool, default=True)

ALLOWED_HOSTS = [
    "*",
    ".railway.app"
]
CSRF_TRUSTED_ORIGINS = [
    "*"
    "https://*.railway.app",
    "http://0.0.0.0:8000",
]

if DEBUG:
    ALLOWED_HOSTS = ["*"]
# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # my installed apps 
    "corsheaders",
    'ninja',
    'ninja_extra',
    "ninja_jwt",
    'ckeditor',
    'ckeditor_uploader', 
    # app
    'courses.apps.CoursesConfig',
    'lessons.apps.LessonsConfig',
    'quizs.apps.QuizsConfig',
    'results.apps.ResultsConfig',
    "users",
    "tasks",
]

AUTH_USER_MODEL = 'users.User'

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Cookie xavfsizligi
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
if DEBUG:
    INSTALLED_APPS.append("whitenoise.runserver_nostatic")

# JWT sozlamalari (optional, defaultlar mavjud)
NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": 5,      # daqiqa
    "REFRESH_TOKEN_LIFETIME": 1440,  # daqiqa (24 soat)
    "AUTH_HEADER_TYPES": ["Bearer"],
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # news
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware", # corse
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME', 'leetcode'),
#         'USER': config('DB_USER', 'leetcode_owner'),
#         'PASSWORD': config('DB_PASSWORD', 'npg_Wzf0CyF2KSmb'),
#         'HOST': config('DB_HOST', 'ep-restless-hat-a5vszuj5-pooler.us-east-2.aws.neon.tech'),
#         'PORT': config('DB_PORT', '5432'),
#         'OPTIONS': {
#             'sslmode': 'require',
#             'connect_timeout': 5,  # 5 sekunddan keyin timeout
#         }
#     }
# }



CORS_ALLOW_ALL_ORIGINS=True

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, os.path.join("template")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME', 'letcode'),
#         'USER': config('DB_USER', 'leetcde_owner'),
#         'PASSWORD': config('DB_PASSWORD', 'npg_Wzf0CyF2KSmb'),
#         'HOST': config('DB_HOST', 'estless-hat-a5vszu.neon.tech'),
#         'PORT': config('DB_PORT', '5432'),
#         'OPTIONS': {
#             'sslmode': 'require',
#             'connect_timeout': 5,  # 5 sekunddan keyin timeout
#         }
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/


from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'uz'

LANGUAGES = [
    ('uz', _('Oʻzbekcha')),
    ('ru', _('Русский')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/



STATIC_URL = 'static/'
MEDIA_URL = 'media/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": BASE_DIR / "media",  # media fayllar saqlanadigan papka
            "base_url": "/media/",          # media fayllarga URL
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#     },
# }
}

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"  
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

