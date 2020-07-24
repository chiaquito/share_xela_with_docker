#from django.contrib import admin
from django.contrib.gis import admin
from .models import UserPointModel

# Register your models here.admin.GeoModelAdmin
#admin.OSMGeoAdmin
admin.site.register(UserPointModel, admin.GeoModelAdmin)