#from django.contrib import admin
from django.contrib.gis import admin
from .models import Profile
# Register your models here.


"""
class ProfileGeoModelAdmin(admin.GeoModelAdmin):

    model = Profile
    #admin_site = 

    def save_model(self, request, obj, form, change):
        update_fields = []

        # True if something changed in model
        # Note that change is False at the very first time
        if change: 
            if form.initial['point'] != form.cleaned_data['point']:
                update_fields.append('point')

            if form.initial['point'] != form.cleaned_data['point']:

        obj.save(update_fields=update_fields)





admin.site.register(Profile, ProfileGeoModelAdmin)
"""
# https://docs.djangoproject.com/en/3.0/ref/contrib/gis/tutorial/#osmgeoadmin
#admin.site.register(Profile, admin.OSMGeoAdmin)
admin.site.register(Profile, admin.GeoModelAdmin)