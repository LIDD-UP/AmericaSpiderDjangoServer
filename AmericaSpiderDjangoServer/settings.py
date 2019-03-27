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

ALLOWED_HOSTS = ['*']

DATA_UPLOAD_MAX_MEMORY_SIZE = None
DATA_UPLOAD_MAX_NUMBER_FIELDS = None
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
        'NAME': 'america_estate_original_db',
        'USER': 'root',
        'PASSWORD': 'saninco123#@!',
        'HOST': '127.0.0.1',
        # 'NAME': 'test',
        # 'USER': 'root',
        # 'PASSWORD': '123456',
        # 'HOST': '127.0.0.1',
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
# MYSQL_DBNAME = 'america_real_estate'
MYSQL_DBNAME = 'test'
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
# server_root_path = r'J:\PycharmProject\AmericaSpiderDjangoServer'
# server_root_path = r'F:\PycharmProject\AmericaSpiderDjangoServer'
# realtor_list_search_criteria = list(set(list(pd.read_csv(server_root_path + r'\tools\realtor_app_list_page_search_criteria_test.csv')['countyStateJoin'])))

# server configure
server_root_path = r'/usr/project/AmericaSpiderDjangoServer'
# server_root_path = r'/home/saninco/lichanghui/AmericaSpiderServer'
realtor_list_search_criteria = list(set(list(pd.read_csv(server_root_path + r'/tools/realtor_app_list_page_search_criteria_test.csv')['countyStateJoin'])))


# 爬虫服务器1
spider_server_domain = "http://106.12.196.106:5000"
# spider_server_domain = "http://127.0.0.1:5000"
# spider_server_domain = "http://192.168.0.211:5000"
# spider_server_domain = "http://127.0.0.1:5001"

spider_detail_start_url = spider_server_domain +'/start_detail_spider/'
spider_list_start_url = spider_server_domain + '/start_list_spider/'
spider_client_get_detail_search_criteria_url = spider_server_domain +'/get_detail_search_criteria/'

# 爬虫服务器2
spider_server_domain2 = "http://106.12.196.86:5000"
# spider_server_domain = "http://192.168.0.211:5000"
# spider_server_domain = "http://127.0.0.1:5001"


spider_detail_start_url2 = spider_server_domain2 +'/start_detail_spider/'
spider_list_start_ur2 = spider_server_domain2 + '/start_list_spider/'
spider_client_get_detail_search_criteria_url2 = spider_server_domain2 +'/get_detail_search_criteria/'

# 爬虫服务器3
spider_server_domain3 = "http://39.106.17.15:5000"

spider_detail_start_url3 = spider_server_domain3 +'/start_detail_spider/'
spider_list_start_ur3 = spider_server_domain3 + '/start_list_spider/'

# list 爬虫执行之前的数据处理之后的url 跳转url
local_ip = 'http://138.197.143.39:8000/spider_server'
# local_ip = 'http://127.0.0.1:8000/spider_server'
redirect_start_list_spider_url = local_ip + '/start_list_spider/'
redirect_post_detail_criteria_to_client_url = local_ip + '/post_detail_criteria_to_client/'
SPIDER_CLIENT_NUMBER = 2




import pymysql
from DBUtils.PooledDB import PooledDB

PYMYSQL_POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=0,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,
    # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host='127.0.0.1',
    port=3306,
    user='root',
    # password='123456',
    # database='america_real_estate',#链接的数据库的名字
    # database='test',
    password='saninco123#@!',
    database='america_estate_original_db',#链接的数据库的名字
    charset='utf8'
)

