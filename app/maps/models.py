#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserPointModel(models.Model):
	#user_name   = models.CharField(max_length=30)
	user_name   = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	point       = models.PointField(srid=4326)
	



	def __str__(self):
		return self.user_name.username