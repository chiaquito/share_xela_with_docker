from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.gis.db import models as geomodels

from feedback.models    import Feedback
from prefecturas.models import Prefectura
from prefecturas.models import Departamento
from prefecturas.models import Municipio
from prefecturas.list_data import adm0_CHOICES, DEPARTAMENTO_CHOICES, MUNICIPIO_CHOICES



from .strings import DEFAULT_PROFILE_DESCRIPTION, DEFAULT_PROFILE_IMAGE


#############
## 参考情報 ##
#############

#https://btj0.com/blog/django/choices/
# (DB値, 読みやすい値)



SEX_CHOICES =((0, "NotSet"),(1, "Hombre"),(2, "Mujer"))



class Profile(models.Model):
	user         = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	adm0         = models.CharField(max_length=15, default="GUATEMALA", choices=adm0_CHOICES)
	adm1         = models.CharField(max_length=15, null=False, choices=DEPARTAMENTO_CHOICES) # 
	adm2         = models.CharField(max_length=30, null=False, choices=MUNICIPIO_CHOICES) # 
	description  = models.TextField(default=DEFAULT_PROFILE_DESCRIPTION)
	feedback     = models.ManyToManyField(Feedback, blank=True, null=True)
	birthday     = models.DateField(null=True, blank=True)
	point        = geomodels.PointField(null=True, blank=True)
	radius       = models.IntegerField(default=0)
	image        = models.ImageField(upload_to="images/" ,null=True, blank=True, default=DEFAULT_PROFILE_IMAGE)
	phonenumber  = PhoneNumberField(null=True, blank=True)
	sex          = models.IntegerField(choices=SEX_CHOICES, default=0)



	def __str__(self):
		return self.user.username



