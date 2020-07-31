from django.urls import path
from .views import ProfileView, CreatingProfileView



app_name = "profiles"


urlpatterns = [
    path('my_account/', ProfileView.as_view(), name='profile'),
    path('profile_create/', CreatingProfileView.as_view(), name='profile_creating'),
]