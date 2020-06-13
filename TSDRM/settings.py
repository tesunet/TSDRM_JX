"""
Django settings for TSDRM project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import djcelery
import pymysql.cursors
import xml.dom.minidom
from xml.dom.minidom import parse, parseString
from lxml import etree


#############################################
# 从config/db_config.xml中读取数据库认证信息 #
#############################################
db_host, db_name, db_user, db_password = '', '', '', ''

try:
    db_config_file = os.path.join(os.path.join(os.path.join(os.getcwd(), "faconstor"), "config"), "db_config.xml")
    # db_config_file = r'D:\Pros\PRO_JX\TSDRM\faconstor\config\db_config.xml'
    with open(db_config_file, "r") as f:
        content = etree.XML(f.read())
        db_config = content.xpath('./DB_CONFIG')
        if db_config:
            db_config = db_config[0]
            db_host = db_config.attrib.get("db_host", "")
            db_name = db_config.attrib.get("db_name", "")
            db_user = db_config.attrib.get("db_user", "")
            db_password = db_config.attrib.get("db_password", "")
except:
    print("获取数据库信息失败。")

# db_host = '192.168.100.154'
# db_name = "js_tesudrm"
# db_user = "root"
# db_password = "password"

# commvault账户
connection = pymysql.connect(host=db_host,
                             user=db_user,
                             password=db_password,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

result = {}
try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT t.content FROM {db_name}.faconstor_vendor t;".format(**{"db_name": db_name})
        cursor.execute(sql)
        result = cursor.fetchone()
finally:
    connection.close()

webaddr = ""
port = ""
usernm = ""
passwd = ""

SQLServerHost = ""
SQLServerUser = ""
SQLServerPasswd = ""
SQLServerDataBase = ""
if result:
    doc = parseString(result["content"])
    try:
        webaddr = (doc.getElementsByTagName("webaddr"))[0].childNodes[0].data
    except:
        pass
    try:
        port = (doc.getElementsByTagName("port"))[0].childNodes[0].data
    except:
        pass
    try:
        usernm = (doc.getElementsByTagName("username"))[0].childNodes[0].data
    except:
        pass
    try:
        passwd = (doc.getElementsByTagName("passwd"))[0].childNodes[0].data
    except:
        pass

    # SQLServer
    try:
        SQLServerHost = (doc.getElementsByTagName("SQLServerHost"))[0].childNodes[0].data
    except:
        pass
    try:
        SQLServerUser = (doc.getElementsByTagName("SQLServerUser"))[0].childNodes[0].data
    except:
        pass
    try:
        SQLServerPasswd = (doc.getElementsByTagName("SQLServerPasswd"))[0].childNodes[0].data
    except:
        pass
    try:
        SQLServerDataBase = (doc.getElementsByTagName("SQLServerDataBase"))[0].childNodes[0].data
    except:
        pass

CVApi_credit = {
    "webaddr": webaddr,
    "port": port,
    "username": usernm,
    "passwd": passwd,
    "token": "",
    "lastlogin": 0
}

# SQLApi
sql_credit = {
    "host": SQLServerHost,
    "user": SQLServerUser,
    "password": SQLServerPasswd,
    "database": SQLServerDataBase,
}

# sql_credit = {
#     "host": "192.168.100.149\COMMVAULT",
#     "user": "sa_cloud",
#     "password": "1qaz@WSX",
#     "database": "CommServ",
# }

djcelery.setup_loader()
# BROKER_URL = 'django://'
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

BROKER_URL = 'redis://:tesunet@127.0.0.1:6379/0'
# BROKER_URL = 'redis://:tesunet@223.247.155.54:6379/0'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
# BROKER_URL = 'amqp://root:password@localhost:5672/myvhost'

CELERY_TIMEZONE = 'Asia/Shanghai'  # 时区
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # 定时任务

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%6n))bx30e&#b+hd!074=4)d!+4w3l(+dy28&%fh&mzv)i@nvr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'faconstor',
    'djcelery',
    'kombu.transport.django',
]

MIDDLEWARE_CLASSES = [
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'TSDRM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates').replace('\\', '/'), ],
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

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

WSGI_APPLICATION = 'TSDRM.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
SITE_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_HOST_USER = 'huangzx@tesunet.com.cn'
EMAIL_HOST_PASSWORD = '1'
EMAIL_PORT = 25

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static")
# ]


# CASHES_DIR = BASE_DIR + os.sep + "faconstor"+ os.sep + "static"+ os.sep + "mem"
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': CASHES_DIR,  # 设置缓存文件的目录
#         'OPTIONS': {
#             'MAX_ENTRIES': 300,  # 最大缓存个数（默认300）
#             'CULL_FREQUENCY': 3,  # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
#         },
#     }
# }

# # 日志系统
# # 创建日志的路径
# LOG_PATH = os.path.join(BASE_DIR, 'log')
# # 如果地址不存在，则自动创建log文件夹
# if not os.path.join(LOG_PATH):
#     os.mkdir(LOG_PATH)
# LOGGING = {
#     "version": 1,
#     # True表示禁用logger
#     "disable_existing_loggers": False,
#     'formatters': {
#         'default': {
#             'format': '%(levelno)s %(module)s %(asctime)s %(message)s ',
#             'datefmt': '%Y-%m-%d %A %H:%M:%S',
#         },
#     },
#
#     'handlers': {
#         'process_handlers': {
#             'level': 'DEBUG',
#             # 日志文件指定为5M, 超过5m重新命名，然后写入新的日志文件
#             'class': 'logging.handlers.RotatingFileHandler',
#             # 指定文件大小
#             'maxBytes': 5 * 1024,
#             # 指定文件地址
#             'filename': '%s/process.txt' % LOG_PATH,
#             'formatter': 'default'
#         },
#         'step_handlers': {
#             'level': 'DEBUG',
#             # 日志文件指定为5M, 超过5m重新命名，然后写入新的日志文件
#             'class': 'logging.handlers.RotatingFileHandler',
#             # 指定文件大小
#             'maxBytes': 5 * 1024,
#             # 指定文件地址
#             'filename': '%s/step.txt' % LOG_PATH,
#             'formatter': 'default'
#         },
#         'script_handlers': {
#             'level': 'DEBUG',
#             # 日志文件指定为5M, 超过5m重新命名，然后写入新的日志文件
#             'class': 'logging.handlers.RotatingFileHandler',
#             # 指定文件大小
#             'maxBytes': 5 * 1024,
#             # 指定文件地址
#             'filename': '%s/script.txt' % LOG_PATH,
#             'formatter': 'default',
#         },
#     },
#     'loggers': {
#         'process': {
#             'handlers': ['process_handlers'],
#             'level': 'INFO'
#         },
#         'step': {
#             'handlers': ['step_handlers'],
#             'level': 'INFO'
#         },
#         'script': {
#             'handlers': ['script_handlers'],
#             'level': 'INFO'
#         }
#     },
#
#     'filters': {
#         # 过滤器
#     }
# }
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console':{
#             'level':'DEBUG',
#             'class':'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'propagate': True,
#             'level':'DEBUG',
#         },
#     }
# }
