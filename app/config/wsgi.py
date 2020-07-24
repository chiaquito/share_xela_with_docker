"""
WSGI config for share_xela project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

#from config.utils import *


from django.core.wsgi import get_wsgi_application

######################################################################
### 'config.settings'から'config.prod_settings'へ変更影響がわからない  ###
######################################################################

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev_settings')


#setDSM()

application = get_wsgi_application()
