from django.urls import path
from .views import ItemDetailView
from .views import ItemListView
from .views import ItemEditView
from .views import ItemListByFavoriteView

from .views import ItemDarLocalListView, ItemDarListView, ItemDeactivateView, ItemQuererPrefecutraListView
from .views import ItemUserListView, ItemSearchView,  ItemQuererListView
from .views import ItemAnuncioListView, ItemAnuncioPrefecturaListView
from .views import ItemFavoriteView

from .views import ItemBuscarHabitacionListView
from .views import ItemBuscarHabitacionLocalListView
from .views import ItemAlquilarHabitacionListView
from .views import ItemAlquilarHabitacionLocalListView
from .views import ItemBuscarTrabajoListView
from .views import ItemBuscarTrabajoLocalListView
from .views import ItemBuscarTrabajadorListView
from .views import ItemBuscarTrabajadorLocalListView

from .views import ItemCategoryListView
from .views import ItemCategoryLocalListView


#from .views import ItemDeleteView ItemFirstCreateView,
#from .views import ItemCreateView
from .views import ItemCreateViewKaizen
from .views import ItemFavoriteViewKaizen



app_name = "items"
urlpatterns = [
	#path('create/', ItemCreateView.as_view(), name='item_create'),
    path('create2/', ItemCreateViewKaizen.as_view(), name='item_create2'),

    path('<int:pk>/delete/', ItemDeactivateView.as_view(), name="item_deactivate"),
    path('list/', ItemListView.as_view(), name='item_list'),
    path('list_dt/', ItemDarListView.as_view(), name='itemdar_list'),
    path('list_dp/', ItemDarLocalListView.as_view(), name='itemdarprefectura_list'),
    path('list_qt/', ItemQuererListView.as_view(), name='itemquerer_list'),
    path('list_qp/', ItemQuererPrefecutraListView.as_view(), name='itemquererprefecutura_list'),
    path('list_at/', ItemAnuncioListView.as_view(), name='itemanuncio_list'),
    path('list_ap/', ItemAnuncioPrefecturaListView.as_view(), name='itemanuncioprefectura_list'),

    path('list_bh/', ItemBuscarHabitacionListView.as_view(), name="BuscarHabitacionList"),
    path('list_bh_local/', ItemBuscarHabitacionLocalListView.as_view(), name="BuscarHabitacionLocalList"),
    path('list/ah/', ItemAlquilarHabitacionListView.as_view(), name="AlquilarHabitacionList"),
    path('list/ah_local/', ItemAlquilarHabitacionLocalListView.as_view(), name="AlquilarHabitacionLocalList"),
    path('list/bt/', ItemBuscarTrabajoListView.as_view(), name="BuscarTrabajoList"),
    path('list/bt_local/', ItemBuscarTrabajoLocalListView.as_view(), name="BuscarTrabajoLocalList"),
    path('list/btr/', ItemBuscarTrabajadorListView.as_view(), name="BuscarTrabajadorList"),
    path('list/btr_local/', ItemBuscarTrabajadorLocalListView.as_view(), name="BuscarTrabajadorLocalList"),

    path("items/category/<int:pk>/items/list/", ItemCategoryListView.as_view(), name="ItemCategoryListView" ),
    path("items/category/<int:pk>/items/list/local/", ItemCategoryLocalListView.as_view(), name="ItemCategoryLocalListView" ),

    path('list_u/',  ItemUserListView.as_view(), name='itemuser_list'),
    path('user/favorite/', ItemListByFavoriteView.as_view(), name='item_list_by_favorite'),
    path('search/', ItemSearchView.as_view(), name='item_search'),
    #path('mylist', MyItemListView.as_view(), name='item_mylist'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    #axiosに変更する
    #path('item/<int:pk>/favorite/', ItemFavoriteView.as_view(), name='item_favorite'),
    path('item/<int:pk>/favorite/', ItemFavoriteViewKaizen.as_view(), name='item_favorite'),

    path('<int:pk>/edit/', ItemEditView.as_view(), name='item_edit'),
    
]

    #path('create/', ItemCreateView.as_view(), name='item_create'),
    #path('create/', ItemFirstCreateView.as_view(), name='item_create'),
    #path('<int:pk>/delete/', ItemDeleteView.as_view(), name="item_delete"),
