from django.urls import path

from feedback.views import ShowFeedbackFormView
from feedback.views import FeedbackView
#from feedback.views import GetDirectMessageByDirectMessageContentForAvisoView


app_name = "feedback"


urlpatterns = [
    
    path('dm/<int:pk>/create/', ShowFeedbackFormView.as_view(), name='create'),
    path('', FeedbackView.as_view(), name='feedback'),
    #path('feedback/<int:pk>/', GetDirectMessageByDirectMessageContentForAvisoView.as_view(), name='get_dm'),
        
]
