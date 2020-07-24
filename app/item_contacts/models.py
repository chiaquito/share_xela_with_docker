from django.db import models

from django.contrib.auth.models import User
from profiles.models import Profile
#from items.models import Item






class ItemContact(models.Model):
	post_user    = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, related_name="post_user")
	#item         = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
	message      = models.TextField()
	timestamp    = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.post_user.user.username


