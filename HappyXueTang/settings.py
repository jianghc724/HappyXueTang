"""
Django settings for HappyXueTang project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import json
import logging
import urllib.parse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configurations load from file
CONFIGS = json.loads(open(os.path.join(BASE_DIR, 'configs.json')).read())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIGS['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIGS['DEBUG']

# SECURITY WARNING: don't run with IGNORE_WECHAT_SIGNATURE turned on in production!
IGNORE_WECHAT_SIGNATURE = CONFIGS['IGNORE_WECHAT_SIGNATURE']

# SECURITY WARNING: keep the WeChat token, appid and secret used in production secret!
WECHAT_TOKEN = CONFIGS['WECHAT_TOKEN']
WECHAT_APPID = CONFIGS['WECHAT_APPID']
WECHAT_SECRET = CONFIGS['WECHAT_SECRET']

API_KEY = CONFIGS['API_KEY']
API_SECRET = CONFIGS['API_SECRET']

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wechat',
    'user',
    'student',
    'teacher',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HappyXueTang.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'HappyXueTang.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': CONFIGS['DB_NAME'],
        'USER': CONFIGS['DB_USER'],
        'PASSWORD': CONFIGS['DB_PASS'],
        'HOST': CONFIGS['DB_HOST'],
        'PORT': CONFIGS['DB_PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_DOMAIN = CONFIGS['SITE_DOMAIN'].rstrip('/')

def get_url(path, params=None):
    full_path = urllib.parse.urljoin(SITE_DOMAIN, path)
    if params:
        return full_path + ('&' if urllib.parse.urlparse(full_path).query else '?') + urllib.parse.urlencode(params)
    else:
        return full_path

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
