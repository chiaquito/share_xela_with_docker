from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import DetailView
from django.contrib.auth.models import User
from .models import UserPointModel 
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry, Point
# Create your views here.

class MapsView(View):

	def get(self, request, *args, **kwargs):
		user = request.user
		my_place    = UserPointModel.objects.get(user_name=User.objects.get(username="ishiharasatomi"))

		pnt = Point(my_place.point.x, my_place.point.y, srid=4326)
		all_objects = UserPointModel.objects.filter(point__distance_lte=(pnt, D(km=2)))
		context = {"all_objects":all_objects}
		return render(request, "maps/list.html",context)


class MapsDetailView(DetailView):

	model = UserPointModel
	template_name = "maps/detail.html"