from django.urls import path
from .views import AvisosAllListView
from .views import AvisosListView
from .views import AvisoCheckingView





app_name = "avisos"

urlpatterns = [
	
    path('all/', AvisosAllListView.as_view(), name='avisos_alllist'),
    path('aviso/', AvisosListView.as_view(), name='avisos_list'),
    path('checking/<int:pk>', AvisoCheckingView.as_view(), name='aviso_check'),
 

]