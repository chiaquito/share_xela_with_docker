from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geomodels
from categories.models import Category
from direct_messages.models import DirectMessage
from profiles.models import Profile
from prefecturas.list_data import adm0_CHOICES, DEPARTAMENTO_CHOICES, MUNICIPIO_CHOICES
from solicitudes.models import Solicitud
from item_contacts.models import ItemContact

from django.utils import timezone

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys





class Item(models.Model):

	user             = models.ForeignKey(User, related_name="user", on_delete=models.PROTECT, null=True)
	title            = models.CharField(max_length=45)
	description      = models.TextField()
	price            = models.IntegerField(default=0)
	category         = models.ForeignKey(Category, on_delete=models.PROTECT)
	adm0             = models.CharField(max_length=15, default="GUATEMALA", choices=adm0_CHOICES)
	adm1             = models.CharField(max_length=15, null=True, choices=DEPARTAMENTO_CHOICES)
	adm2             = models.CharField(max_length=30, null=True, choices=MUNICIPIO_CHOICES)
	point            = geomodels.PointField(null=True, blank=True)
	radius           = models.IntegerField(default=0)
	created_at       = models.DateTimeField(default=timezone.now)
	active           = models.BooleanField(default=True)
	deadline         = models.BooleanField(default=False)
	favorite_users   = models.ManyToManyField(User, blank=True)
	item_contacts    = models.ManyToManyField(ItemContact, blank=True)
	solicitudes      = models.ManyToManyField(Solicitud, blank=True)
	direct_message   = models.ForeignKey(DirectMessage, on_delete=models.PROTECT, null=True, blank=True)	
	image1           = models.ImageField(upload_to="images/" ,null=True, blank=True, default="images/default_item.png")
	image2           = models.ImageField(upload_to="images/" ,null=True, blank=True)
	image3           = models.ImageField(upload_to="images/" ,null=True, blank=True)
	image4           = models.ImageField(upload_to="images/" ,null=True, blank=True)
	image5           = models.ImageField(upload_to="images/" ,null=True, blank=True)
	image6           = models.ImageField(upload_to="images/" ,null=True, blank=True)


	# deadlineをなんの目的で作ったか忘れてしまった
	# deadlineがTrueのとき　アイテム表示が　cerradoになる。

	def __str__(self):
		return self.title


	"""
	def save(self, *args, **kwargs):

		for n in ["1","2","3"]:
			#Opening the uploaded image

			#im = Image.open(self.image1)
			im = Image.open(getattr(self, "image"+n))
			output = BytesIO()

			#Resize/modify the image
			#im = im.resize( (600,600) )


			im.thumbnail((600, 600))

			#after modifications, save it to the output
			#im.save(output, format='JPEG', quality=100)
			im.save(output, format='JPEG', quality=95)
			output.seek(0)

			#change the imagefield value to be the newley modifed image value
			if n == "1":
				self.image1 = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %getattr(self, "image"+n).name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
				#self.image1 = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image+n.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
			elif n == "2":
				self.image2 = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %getattr(self, "image"+n).name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
				#self.image2 = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image+n.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
			elif n == "3":
				self.image3 = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %getattr(self, "image"+n).name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
				#self.image3 = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image+n.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

		super(Item,self).save(*args, **kwargs)
	"""

