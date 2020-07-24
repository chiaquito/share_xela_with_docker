from django.db import models

from django.contrib.auth.models import User
#from profiles.models import Profile


# Create your models here.
class Feedback(models.Model):

    LEVEL_CHOICES = ((5,"満足"), (4,"良い"), (3, "普通"), (3, "不満"), (1, "悪い"),)

    evaluator = models.ForeignKey(User, on_delete=models.PROTECT)
    content   = models.TextField()
    level     = models.IntegerField(choices=LEVEL_CHOICES)

    def __str__(self): 
       return self.evaluator.username 