"""
Django settings for web_services project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f#s6*vk$%!d8vyh!4i1rqnh0dl-p4qnio@_ft8(y7rx*m6-r2y'

from Common.Config import g_ServerConfig
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = g_ServerConfig["WebDebug"]

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	
    'CS3App.apps.Cs3AppConfig',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'Common.middleware.TracbackMiddleware',  # 在Debug=False时，输出脚本错误日志
]

ROOT_URLCONF = 'web_services.urls'

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

WSGI_APPLICATION = 'web_services.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'   : 'mysql.connector.django',
        'NAME'     : g_ServerConfig["WebServerDB"]["Name"],
        'USER'     : g_ServerConfig["WebServerDB"]["User"],
        'PASSWORD' : g_ServerConfig["WebServerDB"]["Password"],
        'HOST'     : g_ServerConfig["WebServerDB"]["Host"],
        'PORT'     : g_ServerConfig["WebServerDB"]["Port"],
        'OPTIONS'  : {
            'autocommit': True,
        }
    },
	#游戏数据库
    'CS3DB' : {
        'ENGINE'   : 'mysql.connector.django',
        'NAME'     : g_ServerConfig["CS3DB"]["Name"],
        'USER'     : g_ServerConfig["CS3DB"]["User"],
        'PASSWORD' : g_ServerConfig["CS3DB"]["Password"],
        'HOST'     : g_ServerConfig["CS3DB"]["Host"],
        'PORT'     : g_ServerConfig["CS3DB"]["Port"],
        'OPTIONS'  : {
            'autocommit': True,
        }
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

#TIME_ZONE = 'UTC
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

#USE_TZ = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

CS_GAME_SERVER_DB = "CS3DB"
CS_SECRET = g_ServerConfig["SignKey"]
CS_OPEN_ACCOUNT_VERIFY = g_ServerConfig["OpenAccountVerify"]

CHARGE_SIGN_TYPE = g_ServerConfig["Charge"]["SignType"]
CHARGE_SIGN_KEY = g_ServerConfig["Charge"]["SignKey"]
CHARGE_VALID_TIME = g_ServerConfig["Charge"]["ValidTime"]
CHARGE_SERVER_GM_PORT = g_ServerConfig["Charge"]["ServerGmPort"]
CHARGE_SERVER_GM_HOSTS = g_ServerConfig["Charge"]["ServerGmHosts"]
CHARGE_SERVER_REQUEST_HOSTS = g_ServerConfig["Charge"]["RequestHosts"]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level'		: 'DEBUG',
            'class'		: 'logging.StreamHandler',
            'formatter'	: 'simple'
        },
        'TimedRotatingFile' : {
            'level' 	: 'DEBUG',
            'class' 	: 'logging.handlers.TimedRotatingFileHandler',
            'filename' 	: g_ServerConfig["WebServicesLogFile"],
            'when'		: 'D',
            'interval' 	: 1,
            'encoding' 	: 'utf-8',
            'formatter'	: 'verbose',
        },
    },
    'loggers': {
        'default': {
            'handlers'	: g_ServerConfig["DefaultHandlers"],
            'level'		: 'DEBUG',
            'propagate' : True,
        },
    }
}