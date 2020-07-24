from django.db import models
from django.contrib.auth.models import User
#from items.models import Item
from profiles.models import Profile
from django.utils import timezone




class DirectMessageContent(models.Model):
	content    = models.TextField()
	profile    = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.content




class DirectMessage(models.Model):
	owner                        = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="owner", null=True)	
	participant                  = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="participant", null=True)
	direct_message_contents      = models.ManyToManyField(DirectMessageContent)
	is_feedbacked_by_owner       = models.BooleanField(default=False)
	is_feedbacked_by_participant = models.BooleanField(default=False)
	created_at                   = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.owner.user.username
