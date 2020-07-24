import os
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost","10.0.2.2", "127.0.0.1", "192.168.1.6",  'testserver',]


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