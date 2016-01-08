"""
Django settings for gift project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*(fpy)%b*mnc(#t5r)xw63_f8yc5muba!w1ulky1zx2m-%$7qf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'tastypie'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
)

ROOT_URLCONF = 'gift.urls'

WSGI_APPLICATION = 'gift.wsgi.application'

#AUTH_PROFILE_MODULE = 'app.UserProfile'

# Databases
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'de94rmc93831fg',
        'USER': 'eljynyyvsrnizg',
        'PASSWORD': '9pQM_Z20wr0QvRnD01cYGsJWwK',
        'HOST': 'ec2-23-23-199-181.compute-1.amazonaws.com'
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

STATIC_URL = '/static/'

MEDIA_ROOT = '/var/django/gift/assets/'
MEDIA_URL = '/assets/'

ACCOUNT_ACTIVATION_DAYS = 7

# CORS
CORS_ORIGIN_ALLOW_ALL   = True
CORS_ALLOW_CREDENTIALS  = True
SESSION_COOKIE_HTTPONLY = False

# Heroku Setup

# Parse database configuration from $DATABASE_URL
#import dj_database_url
#DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']





# OCR Web Service Params
OCR_DEBUG = False
OCR_USER_NAME = "NICKCRAFFORD"
OCR_LICENSE_CODE = "2FF2AE76-A4CE-4A6A-A24F-D7C3D39794B8"

SUIT_CONFIG = {
    'ADMIN_NAME': 'Gift2Redeem'
}

MAIL_SERVER = "smtp.gmail.com"
MAIL_USERNAME = "g2r.test@gmail.com"
MAIL_PASSWORD = "nutech123"



SMS_API_AUTH_CODE = "cYNKz2Fxqbi1V-06KKKZFw"