"""
Django settings for myschool project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import environ
import os
from pathlib import Path

from django.contrib import messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9ti=2j!h7x&e15^mh-0)5i$*bhhcgu=f7=zgy%r@mx$&$maxat'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'account',
    'teacher',
    'academic',
    'dashboard',
    'student',

    # APP TIERS
    'ckeditor',  # ckeditor for blog content
    'crispy_forms',  # crispy
    'crispy_bootstrap5',  # crispy
    'ckeditor_uploader',
    'taggit',
    'widget_tweaks',
    'active_link',  # active link
    'rolepermissions',
    'import_export',
    'django_filters',
    'result',
    'django_file_form',
    'verify_email.apps.VerifyEmailConfig',  # verify email

]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger'
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myschool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'myschool.wsgi.application'

AUTH_USER_MODEL = 'account.USER'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = ''  # Route defined in dashboard/urls.py
LOGOUT_REDIRECT_URL = 'home:home'  # Route defined in home/urls.py

# for permission management
ROLEPERMISSIONS_MODULE = 'myschool.roles'
# ROLEPERMISSIONS_REGISTER_ADMIN = True

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

CKEDITOR_UPLOAD_PATH = 'ck-uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ['codesnippet', 'markdown'], 'width': '100%',
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ###########################################################
# ###########################################################
# SMTP configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'MbkSite<staff@opentransport.org>'

# ##############################################
# Email verify settings
EXPIRE_AFTER = "1h"
HTML_MESSAGE_TEMPLATE = 'email/email_verification.html'
