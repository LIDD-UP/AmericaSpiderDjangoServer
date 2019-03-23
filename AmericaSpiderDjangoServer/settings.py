"""
Django settings for AmericaSpiderDjangoServer project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')k@)(o_3lk9qr(j8$)_yk*17x)-ny82#24f%glin7&b=$w%okl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'spider_server',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AmericaSpiderDjangoServer.urls'

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

WSGI_APPLICATION = 'AmericaSpiderDjangoServer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


# american server config

# MYSQL_HOST = '127.0.0.1'
# MYSQL_PORT = 3306
# MYSQL_DBNAME = 'america_estate_original_db'
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = 'saninco123#@!'

# local windows mysql config
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_DBNAME = 'america_real_estate'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'

# local linux mysql config
# MYSQL_HOST = '192.168.0.65'
# MYSQL_PORT = 3306
# MYSQL_DBNAME = 'america_estate_data_db'
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = 'saninco123#@!'



import pandas as pd

# local configure
# server_root_path = r'F:\PycharmProject\AmericaSpiderServer'
server_root_path = r'J:\PycharmProject\AmericaSpiderDjangoServer'
# realtor_list_search_criteria = list(set(list(pd.read_csv(server_root_path + r'\tools\realtor_app_list_page_search_criteria_test.csv')['countyStateJoin'])))

# server configure
# server_root_path = r'/usr/project/AmericaSpiderServer'
# server_root_path = r'/home/saninco/lichanghui/AmericaSpiderServer'
realtor_list_search_criteria = list(set(list(pd.read_csv(server_root_path + r'/tools/realtor_app_list_page_search_criteria_test.csv')['countyStateJoin'])))


spider_server_domain = "http://106.12.196.106:5000"
# spider_server_domain = "http://192.168.0.211:5000"
# spider_server_domain = "http://127.0.0.1:5001"

spider_detail_start_url = spider_server_domain +'/start_detail_spider/'
spider_list_start_url = spider_server_domain + '/start_list_spider/'


spider_server_domain2 = "http://106.12.196.86:5000"
# spider_server_domain = "http://192.168.0.211:5000"
# spider_server_domain = "http://127.0.0.1:5001"

spider_detail_start_url2 = spider_server_domain2 +'/start_detail_spider/'
spider_list_start_ur2 = spider_server_domain2 + '/start_list_spider/'
