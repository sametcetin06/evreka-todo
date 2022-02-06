from core.env.settings import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'evrekadb',
        'USER': 'evrekauser',
        'PASSWORD': 'evrekapassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

