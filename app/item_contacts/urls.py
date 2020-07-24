from django.urls import path
from .views import ItemByItemContactView
from .views import ItemContactView
#from .views import ItemDeleteView ItemFirstCreateView,



app_name = "item_contacts"

urlpatterns = [
	path('itemcontact/', ItemContactView.as_view(), name='ItemContactView'),
    path('itemcontact/<int:pk>', ItemByItemContactView.as_view(), name='item_itemcontact'),
        
]