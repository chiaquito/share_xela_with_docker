from django.db import models

from django.contrib.auth.models import User
#from profiles.models import Profile


# Create your models here.
class Feedback(models.Model):

    LEVEL_CHOICES = ((5,"Satisfecho"), (4,"Bueno"), (3, "Ordinario"), (3, "Insatisfecho"), (1, "Malo"),)
    evaluator = models.ForeignKey(User, on_delete=models.PROTECT)
    content   = models.CharField(max_length=50, null=True, blank=True)
    level     = models.IntegerField(choices=LEVEL_CHOICES)

    def __str__(self): 
       return self.evaluator.username 