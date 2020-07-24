from django.shortcuts import render
from prefecturas.models import Prefectura
from django.views.generic import View
from djgeojson.views import GeoJSONLayerView
import json

# Create your views here.


class PrefecturaListView(View):
	def get(self, request, *args, **kwargs):
		context = {}
		prefecturas_objects = Prefectura.objects.all().first()
		context["objects"]  = prefecturas_objects
		coordinates = prefecturas_objects.mpoly.geojson
		print(type(coordinates))
		coordinates = json.loads(coordinates)['coordinates'][0][0]
		print(type(coordinates))
		
		#print(type(coordinates))
		#["coordinates"]
		context["coordinates"] = coordinates 
		#print(dir(prefecturas_objects.mpoly))

		return render(request, 'prefecturas/prefecturas_list.html', context)



class PolygonLayer(GeoJSONLayerView):
	geometry_field = "mpoly"

