from django.urls import path
from contacts.views import ContactView

app_name = "contacts"

urlpatterns = [

    path('inquiries/', ContactView.as_view(), name='inquiries'),

]
