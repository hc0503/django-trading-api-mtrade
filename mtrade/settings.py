"""
Django settings for mtrade project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from mtrade.infrastructure.logger.services import CustomisedJSONFormatter
from logging_utilities.formatters.extra_formatter import ExtraFormatter

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vj=i(8=$tztxua$@wo3@lfgm1k330n3)letp21is3#u9(ul8i$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DEBUG']

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

AUTH_USER_MODEL = 'users.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mtrade.domain.users',
    'mtrade.domain.market',
    'app_zero.apps.AppZeroConfig',
    'rest_framework',
    'drf_spectacular',
    'django_extensions',
    'mtrade.infrastructure.logger',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_structlog.middlewares.RequestMiddleware',
]

ROOT_URLCONF = 'mtrade.interface.urls'

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

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

SPECTACULAR_DESCRIPTION = """
This is an interactive view of the MTrade API, please log in by clicking the "Authorize" button in order to test it.

This view should **NOT** be deployed to production.
"""

SPECTACULAR_SETTINGS = {
    'TITLE': 'MTrade API',
    'DESCRIPTION': SPECTACULAR_DESCRIPTION,
    'TOS': None,
    # Optional: MAY contain "name", "url", "email"
    'VERSION': '0.1.0',
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
}

WSGI_APPLICATION = 'mtrade.drivers.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.environ['DB_ENGINE'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Logging (export log to JSON)
# https://pypi.org/project/JSON-log-formatter/

# Loggin (export log to text with extra)
# https://pypi.org/project/logging-utilities/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
			'()': CustomisedJSONFormatter,
		},
        'app': {
            '()': ExtraFormatter,
            'format': 'level: "%(levelname)s"\t msg: "%(message)s"\t module: "%(name)s.%(funcName)s"\t time: "%(asctime)s"',
            'extra_fmt': '\t extra: %s',
        },
    },
    'handlers': {
        'json_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/log.json',
            'formatter': 'json',
		},
        'app_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/log.log',
            'formatter': 'app',
        }
    },
    'loggers': {
        '': {
			'handlers': ['json_file', 'app_file'],
            'level': 'DEBUG',
            # required to avoid double logging with root logger
            'propagate': False,
		},
    },
}
