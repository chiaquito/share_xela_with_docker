from django.urls import path
from contacts.views import ContactView
#from .views import ItemDeleteView ItemFirstCreateView,


app_name = "contacts"

urlpatterns = [
	
    path('inquiries/', ContactView.as_view(), name='inquiries'),
    #path('check/', ItemCheckView.as_view(), name='item_check'),
    
]