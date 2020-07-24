from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
#from items.models import Item
from profiles.models import Profile
from direct_messages.models import DirectMessage
from direct_messages.models import DirectMessageContent



# Create your models here.

class Solicitud(models.Model):

	#item           = models.ForeignKey(Item, on_delete=models.PROTECT)
	#solicitud_user = models.ForeignKey(User, on_delete=models.PROTECT)
	applicant      = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True)
	message        = models.TextField(null=True)
	timestamp      = models.DateTimeField(auto_now_add=True)
	accepted       = models.BooleanField(default=False)


	def __str__(self):
		return str(self.applicant)






