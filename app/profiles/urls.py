from django.urls import path
from .views import ProfileView, CreatingProfileView
from .views import ProfileShowToOthersView


app_name = "profiles"


urlpatterns = [
    path('my_account/', ProfileView.as_view(), name='profile'),
    path('profile_create/', CreatingProfileView.as_view(), name='profile_creating'),
    path('user/<int:pk>/profile/', ProfileShowToOthersView.as_view(), name='profile_show'),
]