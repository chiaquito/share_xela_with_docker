from django.urls import path
from .views import SolicitudInputView
from .views import SolicitudListView
from .views import SolicitudSelectView
from .views import GetSolicitudListForAvisoView

app_name = "solicitudes"

urlpatterns = [
	
    path('item/<int:pk>/', SolicitudInputView.as_view(), name='solicitud_input'),
    path('item/<int:pk>/solicitud_list/', SolicitudListView.as_view(), name='solicitud_list'),
    path('solicitud/<int:pk>/select/', SolicitudSelectView.as_view(), name='solicitud_decision'),
    path('solicitud/<int:pk>/', GetSolicitudListForAvisoView.as_view(), name='get_solicitud'),
 
]



