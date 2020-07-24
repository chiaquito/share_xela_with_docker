from django.db import models

from django.contrib.auth.models import User
# Create your models here.




class DeviceToken(models.Model):

    user  = models.OneToOneField(User, on_delete=models.PROTECT)
    device_token = models.CharField(max_length=200, null=True) ##実際は152文字だけれども具体的な数字を確認することができなかったので200字とした


    def __str__(self):
        return self.user.username