import os
from .base import *
import environ 


env_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_file = os.path.join(env_dir, ".env")
env = environ.Env()
env.read_env(env_file)



DEBUG = False

ALLOWED_HOSTS = [
    'sharexela.ga',
    '153.126.194.171',
    '144.202.23.188',
    "192.168.1.6",
    '127.0.0.1'
    ]


DATABASES = {
    'default': {        
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgis_test',
        'PORT': '5432',
        'USER': 'geodjango_user',
        'PASSWORD': 'geodjango1990',
        'HOST': os.environ.get('DATABASE_HOST', default=''),
    }
}




# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-MX'
# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Guatemala'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


# DOCKER_production環境とproduction環境でディレクトリを使い分ける
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

LAUNCH_ENV = os.environ.get("LAUNCH_ENV", default='no_docker')

if LAUNCH_ENV == 'no_docker':
    MEDIA_ROOT = '/usr/share/nginx/html/media/'
    STATIC_ROOT = '/home/chiaki/sharexela_src/static_root/'
    STATICFILES_DIRS = ['/home/chiaki/sharexela_src/static/', ]

elif LAUNCH_ENV == 'DOCKER':
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]


# STATIC_ROOT   = '/usr/share/nginx/html/static/'
# STATICFILES_DIRS = '/usr/share/nginx/html/static'


###########################
### EMAIL BACKEND        ##
###########################

EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'


###########################
## LOGGING              ###
###########################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"

        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/sharexela.log',
            'formatter':'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
        'blog': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}
