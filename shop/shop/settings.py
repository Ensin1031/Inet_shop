"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

import django_redis.cache
from decouple import config

import django.core.mail.backends.smtp

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CART_SESSION_ID = 'cart'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'mptt',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',
    'widget_tweaks',
    'bootstrap4',
    'phonenumber_field',
    'main_app.apps.MainAppConfig',
    'accounts.apps.AccountsConfig',
    'shopping.apps.ShoppingConfig',
    'orders.apps.OrdersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'orders.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'shop.wsgi.application'

CASHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/0'
    }
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('HOST', default='localhost'),
        'PORT': config('PORT', default=5432)
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'    # 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # указываем путь к папке, где хранятся все статические файлы

STATICFILES_DIRS = [                           # переменная со списком путей с дополнительными папками со статикой
    os.path.join(BASE_DIR, 'shop/static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')    # указываем корневой каталог для медиа файлов

MEDIA_URL = '/media/'   # нужен для построения пути при загрузке файлов

INTERNAL_IPS = ["127.0.0.1"]

SITE_ID = 1

ADMINS = [('admin', 'admin@gmail.com'), ]

SERVER_EMAIL = 'root@localhost'

AUTH_USER_MODEL = 'accounts.ShopUser' # используемая модель пользователя

LOGIN_URL = '/accounts/login/' # путь авторизации

LOGIN_REDIRECT_URL = '/' # путь редиректа при входе в аккаунт

LOGOUT_REDIRECT_URL = '/' # путь редиректа при выходе из аккаунта

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # класс-отправитель писем по протоколу SMTP

DEFAULT_FROM_EMAIL = 'webmaster@localhost' # email отправителя (по умолчанию)

EMAIL_HOST = 'localhost'
#TODO --> 1025
EMAIL_PORT = 1025 # номер TCP-порта (в cmd запустить: python -m smtpd -n -c DebuggingServer localhost:1025,
                  # для активации пользователя запустить ссылку из терминала http://localhost:8000/accounts/register/activate/username:...)

# celery -A shop worker -l INFO -P eventlet

BROKER_URL = 'redis://localhost:6379/0'

CELERY_BROKER_URL = 'redis://localhost:6379/0'

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

CELERY_ACCEPT_CONTENT = ['application/json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'