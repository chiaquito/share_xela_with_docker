"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.contrib.gis import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import allauth.urls
import api.urls
import avisos.urls
import contacts.urls
import direct_messages.urls
import feedback.urls
import item_contacts.urls
import items.urls
import maps.urls
import mypages.urls
import prefecturas.urls
import profiles.urls
import solicitudes.urls

from .views import HomeView, HowtoView, UsernameChangeView, EmailAddressChangeView, PrivacyView, CheckProfileView
from .views import HomeKaizenView
from .views import ListMyDataView


urlpatterns = [
    #path('', HomeView.as_view(), name='home'),
    path('',HomeKaizenView.as_view(), name='home'),
    path('check_profile/', CheckProfileView.as_view(), name='check_profile'),
    path('howto/', HowtoView.as_view(), name='howto'),
    path('username_change/', UsernameChangeView.as_view(), name='username_change'),
    path('email_change/', EmailAddressChangeView.as_view(), name='email_change'),
    path('privacy', PrivacyView.as_view(), name='privacy'),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('avisos/', include(avisos.urls)),
    path('contacts/', include(contacts.urls)),
    path('direct_messages/', include(direct_messages.urls)),
    path('feedback/', include(feedback.urls)),
    path('maps/', include(maps.urls)),
    path('item_contacts/', include(item_contacts.urls)),
    path('items/', include(items.urls)),
    path('mypages/', include(mypages.urls)),
    path('prefecturas/', include(prefecturas.urls)),
    path('profiles/', include(profiles.urls)),
    path('solicitudes/', include(solicitudes.urls)),
    path('listing/shuppin/', ListMyDataView.as_view()),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)