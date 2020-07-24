from django.urls import path
from .views import  MyItemListView


app_name = "mypages"

urlpatterns = [
    path('mylist', MyItemListView.as_view(), name='item_mylist'),
]