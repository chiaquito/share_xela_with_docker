
from django.urls import path
from .views import MapsView, MapsDetailView

urlpatterns = [
    path('', MapsView.as_view()),
    path('<int:pk>',MapsDetailView.as_view())
]