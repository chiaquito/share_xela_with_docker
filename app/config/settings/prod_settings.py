import os
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['sharexela.ga','153.126.194.171','144.202.23.188', '127.0.0.1']


DATABASES = {
    'default': {        
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgis_test',
        'PORT': '5432',
        'USER': 'geodjango_user',
        'PASSWORD': 'geodjango1990',
    }
}




# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-MX'
#TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Guatemala'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL    = '/static/'
STATIC_ROOT   = os.path.join(BASE_DIR, 'static_root')
#STATIC_ROOT   = '/usr/share/nginx/html/static/'

MEDIA_URL     = '/media/'
#MEDIA_ROOT    = '/usr/share/nginx/html/media/'
MEDIA_ROOT    = os.path.join(BASE_DIR, 'media_root')

STATICFILES_DIRS = [ os.path.join(BASE_DIR,'static'),]
#STATICFILES_DIRS = '/usr/share/nginx/html/static'




###########################
### EMAIL BACKEND        ##
###########################


EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'

