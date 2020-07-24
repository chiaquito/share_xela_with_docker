import os
from .base import *
import environ 


env_dir  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_file = os.path.join(env_dir, ".env")
env = environ.Env()
env.read_env(env_file)





DEBUG = True
ALLOWED_HOSTS = ["localhost","10.0.2.2", "127.0.0.1", "192.168.1.6",  'testserver',]





DATABASES = {
    'default': {
        'ENGINE': os.environ.get("DATABASE_ENGINE"),
        'NAME': os.environ.get("DATABASE_DB"),
        'PORT': os.environ.get("DATABASE_PORT"),
        'USER': os.environ.get("DATABASE_USER"),
        'HOST': os.environ.get('DATABASE_HOST', default='localhost'),
        'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
        'TEST':{"NAME" : "test_postgis_db"},
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgis_test',
        'PORT': '5432',
        'USER': 'geodjango_user',
        'PASSWORD': 'geodjango1990',
        'TEST':{"NAME" : "test_postgis_db"},
    }
}
"""





# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Guatemala'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL       = '/static/'
STATIC_ROOT      = (os.path.join(BASE_DIR, 'config', 'static'))

MEDIA_URL        = '/media/'
MEDIA_ROOT       = (os.path.join(BASE_DIR, 'config', 'media'))

STATICFILES_DIRS = [ os.path.join(BASE_DIR,'static'),]






###########################
### EMAIL BACKEND        ##
###########################


#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'