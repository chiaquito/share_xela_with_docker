
from django.contrib import admin
from .models import Prefectura
from .models import Municipio
from .models import Departamento
from .models import RegionClassed

# Register your models here.







class PrefecturaModelAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields if f.name != "geom"]
        
admin.site.register(Prefectura, PrefecturaModelAdmin)





class MunicipioModelAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields if f.name != "geom"]

admin.site.register(Municipio, MunicipioModelAdmin)




class DepartamentoModelAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields if f.name != "geom"]

admin.site.register(Departamento, DepartamentoModelAdmin)




class RegionClassedModelAdmin(admin.ModelAdmin):
    readonly_fields = ('departamento', 'municipios',)


admin.site.register(RegionClassed, RegionClassedModelAdmin)


