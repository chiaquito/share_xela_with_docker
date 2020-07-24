from django.urls import path
from .views import PrefecturaListView
#from djgeojson.views import GeoJSONLayerView
from .views import PolygonLayer
from .models import Prefectura


app_name = "prefecturas"

urlpatterns = [
    path('list/', PrefecturaListView.as_view(), name='prefecturas_list'),
    #path('mylist', MyItemListView.as_view(), name='item_mylist'),
    path('data/', PolygonLayer.as_view(model=Prefectura), name="data" ),
]

#path('data/', PolygonLayer.as_view(model=Prefectura, properties=('adm2_es',)), name="data" ),