from django.contrib import admin
from .models import Category
# Register your models here.



class CategoryAdmin(admin.ModelAdmin):
    #readonly_fields = ('name',)
    readonly_fields = ()

admin.site.register(Category, CategoryAdmin)