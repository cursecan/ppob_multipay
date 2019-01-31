from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

RB_URL = 'https://rajabiller.fastpay.co.id/transaksi/json_devel.php'