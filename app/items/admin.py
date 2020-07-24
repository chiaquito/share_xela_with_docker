#from django.contrib import admin
from .models import Item
# Register your models here.
from django.contrib.gis import admin


admin.site.register(Item, admin.GeoModelAdmin)