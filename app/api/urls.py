from django.urls import path


from api.views import ItemContactListAPIView
from api.views import ItemContactAPIView
from api.views import ItemContactListByContactObjPKAPIView
from api.views import TestAPIView
from api.views import TestAPI2View
from api.views import AreaSettingApiView
from api.views import AreaSettingWithGeoJsonApiView
from api.views import AvisosAllListAPIView
from api.views import CheckAuthTokenView
from api.views import ContactAPIView
from api.views import DirectMessageContentListAPIView
from api.views import DirectMessageContentAPIView
from api.views import ItemObjByDirectMessageContentObjPKAPIView
from api.views import PrefecturaAPIView
from api.views import SolicitudAPIView
from api.views import SolicitudListAPIView
from api.views import SolicitudListAPIViewBySolicitudObjAPIView
from api.views import SubsolicitudListOrDirectMessageListAPIView
from api.views import GetRegionDataByPointAPIView

from api.views import CustomeRegisterView


from api.Views.fcm_views import DeviceTokenDealAPIVeiw
from api.Views.profile_views import ProfileAPIView
from api.Views.item_views import ItemListAPIView
from api.Views.item_views import ItemHomeListAPIView
from api.Views.item_views import ItemDetailSerializerAPIView
from api.Views.item_views import MyItemListSerializerAPIView
#from api.Views.item_views import ItemCreateAPIView
from api.Views.item_views import ItemCreateAPIViewMulti
from api.Views.item_views import ItemFavoriteAPIView
from api.Views.item_views import ItemFavoriteListAPIVIiew
from api.Views.item_views import ItemCategoryListAPIView
from api.Views.item_views import ItemCategoryLocalListAPIView








app_name = "api"

urlpatterns = [	

    #User registration
    path("custom/rest-auth/registration/",CustomeRegisterView.as_view(),),

    #DeviceToken
    path('fcm/user/device_token/',DeviceTokenDealAPIVeiw.as_view()),

    #Item
    path('items/list/', ItemListAPIView.as_view(), name='item_list'),
    path('items/home/list/', ItemHomeListAPIView.as_view(), name='item_home_list'),
    path('items/category/<int:pk>/items/list/', ItemCategoryListAPIView.as_view(),),
    path('items/category/<int:pk>/items/list/local/', ItemCategoryLocalListAPIView.as_view(),),
    path('items/<int:pk>/', ItemDetailSerializerAPIView.as_view(), name="item_detail"),
    path('items/user/item_favorite_list/', ItemFavoriteListAPIVIiew.as_view()),
    path('items/test/', TestAPIView.as_view(),),
    path('items/test2/',TestAPI2View.as_view(),),
    #path('item_create/', ItemCreateAPIView.as_view()),
    path('item_create_1/', ItemCreateAPIViewMulti.as_view()),
    path('item/<int:pk>/favorite/', ItemFavoriteAPIView.as_view()),

    #ItemContact
    path('item/<int:pk>/item_contacts/list/', ItemContactListAPIView.as_view()),
    path('item_contacts/', ItemContactAPIView.as_view()),
    path('item_contact/<int:pk>/item_contacts/', ItemContactListByContactObjPKAPIView.as_view(), name="ItemContactListByContactObjPKAPIView"),

    path('tokencheck/',CheckAuthTokenView.as_view(),),
    path('area_setting/', AreaSettingApiView.as_view(),),
    path('area_setting_geo/',AreaSettingWithGeoJsonApiView.as_view()),
    path('avisos/list/', AvisosAllListAPIView.as_view(),),
    path('contacts/', ContactAPIView.as_view(),),
    #directMessage
    path('item/<int:pk>/direct_message_content_list/', DirectMessageContentListAPIView.as_view(), name='DirectMessageContentListAPIView'),
    path('direct_message_content/<int:pk>/', DirectMessageContentAPIView.as_view(), name='DirectMessageContentAPIView'),
    path('direct_message_content/<int:pk>/ritem/', ItemObjByDirectMessageContentObjPKAPIView.as_view()),
    
    
    path('mylist/', MyItemListSerializerAPIView.as_view()),
    path('prefecturas/', PrefecturaAPIView.as_view()),
    path('profiles/', ProfileAPIView.as_view(),),

    #Solicitud
    path('solicitudes/item/<int:pk>/',SolicitudAPIView.as_view(),),  #POSTメソッドにつなぐ
    path('solicitud/<int:pk>/',SolicitudAPIView.as_view()), #GET,PATCHにつなぐ
    path('solicitud_list/<int:pk>/',SolicitudListAPIView.as_view(), name='SolicitudListAPIView' ),
    path('solicitudes/solicitud/<int:pk>/solicitud_list/', SolicitudListAPIViewBySolicitudObjAPIView.as_view()),
    path('sub_solicitud_direct/<int:pk>/',SubsolicitudListOrDirectMessageListAPIView.as_view(), name='SubsolicitudListOrDirectMessageListAPIView'),

    path('util/region/', GetRegionDataByPointAPIView.as_view()),

    path("multipoly_test/", PrefecturaAPIView.as_view()),
    
]





"""
#もし以下を使うならconstants.pyで定義すること。urls.pyの内容はviews.pyでは呼び出すことはできないっぽい

class RedirectAPIName(object):

    SolicitudListAPIView = 'api:solicitudesList' 
"""
