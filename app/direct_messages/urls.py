from django.urls import path
from .views import GetDirectMessageByUserListView
from .views import DirectMessageDetailView
from .views import GetDirectMessageByDirectMessageContentForAvisoView


app_name = "direct_messages"


urlpatterns = [
	
    path('list/', GetDirectMessageByUserListView.as_view(), name='dm_list'),
    path('<int:pk>/', DirectMessageDetailView.as_view(), name='dm_detail'),
    path('dmcontent/<int:pk>/', GetDirectMessageByDirectMessageContentForAvisoView.as_view(), name='get_dm'),
    
        
]