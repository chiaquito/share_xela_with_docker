from django.db import models
from django.contrib.gis.db import models
# Create your models here.



#Guatemalaのデータは以下にある
# https://data.humdata.org/search?q=guatemala&ext_search_source=main-nav

#利用ソース
# https://data.humdata.org/dataset/guatemala-administrative-level-0-national-1-departments-and-2-municipalities




# Municipioのデータであることが判明
class Prefectura(models.Model):
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    adm2_es    = models.CharField(max_length=50) # Municipio
    adm2_pcode = models.CharField(max_length=50)
    adm2_ref   = models.CharField(max_length=50)
    adm2alt1es = models.CharField(max_length=50, null=True)
    adm2alt2es = models.CharField(max_length=50, null=True)
    adm1_es    = models.CharField(max_length=50) # Departamento
    adm1_pcode = models.CharField(max_length=50)
    adm0_es    = models.CharField(max_length=50) # Pais
    adm0_pcode = models.CharField(max_length=50)
    date       = models.DateField()
    validon    = models.DateField()
    validto    = models.DateField(null=True)
    mpoly      = models.MultiPolygonField()



    def __str__(self):
        return self.adm2_es





class Municipio(models.Model):
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    adm2_es    = models.CharField(max_length=50) # Municipio
    adm2_pcode = models.CharField(max_length=50)
    adm2_ref   = models.CharField(max_length=50)
    adm2alt1es = models.CharField(max_length=50, null=True)
    adm2alt2es = models.CharField(max_length=50, null=True)
    adm1_es    = models.CharField(max_length=50) # Departamento
    adm1_pcode = models.CharField(max_length=50)
    adm0_es    = models.CharField(max_length=50) # Pais
    adm0_pcode = models.CharField(max_length=50)
    date       = models.DateField()
    validon    = models.DateField()
    validto    = models.DateField(null=True, blank=True)
    geom       = models.MultiPolygonField()

    def __str__(self):
        return self.adm2_es




class Departamento(models.Model):
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    adm1_es    = models.CharField(max_length=50)
    adm1_pcode = models.CharField(max_length=50)
    adm1_ref   = models.CharField(max_length=50)
    adm1alt1es = models.CharField(max_length=50)
    adm1alt2es = models.CharField(max_length=50)
    adm0_es    = models.CharField(max_length=50)
    adm0_pcode = models.CharField(max_length=50)
    date       = models.DateField()
    validon    = models.DateField()
    validto    = models.DateField(null=True, blank=True)
    geom       = models.PolygonField()

    def __str__(self):
        return self.adm1_es



class RegionClassed(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    municipios   = models.ManyToManyField(Municipio)

    def __str__(self):
        return self.departamento.adm1_es


