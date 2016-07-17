"""
Django settings for ad project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h8vejokn)4j)65%rienw!o76qv7s62!&ax79ov1jcznsu6%uf#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
 

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    #'django.contrib.staticfiles', 
    'administration',
    'base',
    'center',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'statmiddleware.StatMiddleware.Device',
)

ROOT_URLCONF = 'ad.urls'

WSGI_APPLICATION = 'ad.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
'''
DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ad',
        'USER': 'root',
        'PASSWORD': 'sqlroot',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on localhost
        'PORT': '3306',
    } 
}
'''
DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.postgresql',# this is for 1.9?
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'adshow',
        'USER': 'aduser',
        'PASSWORD': 'Jason0322%',
        'HOST': '101.201.43.223',
        'PORT': '5432',
    },
    
    'web': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ad',
        'USER': 'root',
        'PASSWORD': 'sqlroot',
        'HOST': 'localhost',  
        'PORT': '3306',
    } 
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR,'static').replace('\\','/') 
STATIC_URL = '/static/'

#MEDIA_ROOT    = '/portrait/'
MEDIA_ROOT    = os.path.join( BASE_DIR ,'../media').replace('\\','/')

MEDIA_URL = '/media/' 

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static") ,MEDIA_ROOT
]


OSS_URL = 'http://creative-gallery.oss-cn-beijing.aliyuncs.com'
THUMBNAIL_URL = 'http://creative-gallery.oss-cn-beijing.aliyuncs.com/thumbnail/'
CREATIVE_URL  = 'http://creative-gallery.oss-cn-beijing.aliyuncs.com/creative/'
NETWORK_URL  = '/logo/'
THUMBNAIL_ROOT = os.path.join(BASE_DIR,'thumbnails').replace('\\','/')
#THUMBNAIL_ROOT = os.path.join('/root/web/','thumbnails').replace('\\','/')
 
 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),os.path.join(BASE_DIR, 'frame'),os.path.join(BASE_DIR, 'administration'),],
        'APP_DIRS': True,
        'OPTIONS': {
        'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.core.context_processors.request",                
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
            ],
        },
    },
]
 
SMTP_SERVER         ='smtp.mxhichina.com' #SMTP server IP address
SMTP_SERVER_USER    ='service@adjason.com'  
SMTP_SERVER_PWD     ='Ad889886'

AUTH_USER_MODEL = 'administration.User'

DATABASE_ROUTERS = ['dbrouter.WebSiteRouter.WebSiteRouter']

EMAIL_SWITCH  =   True

LOGGER         = 'ad_log'
LOGGER_HANDLER = 'ad.log'

logger    = logging.getLogger(LOGGER)
handler   = logging.FileHandler(LOGGER_HANDLER)
formatter = logging.Formatter('%(asctime)-25s  %(levelname)-10s %(user)-10s %(funcName)-10s %(lineno)d  %(message)s ')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(DEBUG)

SUPPORTOR_EMAIL = '281475120@163.com'

LOGIN_URL = '/user/login'