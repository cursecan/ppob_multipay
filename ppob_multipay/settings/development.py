from .base import *
from decouple import config, Csv

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# JWT Auth
# https://getblimp.github.io/django-rest-framework-jwt/
JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=config('JWT_EXP', cast=int)),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(minutes=config('JWT_REFRESH_EXP', cast=int)),
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWD'),
        'HOST': config('DB_HOST'),
        'PORT': '',
    }
}

RB_URL = 'https://rajabiller.fastpay.co.id/transaksi/json_devel.php'