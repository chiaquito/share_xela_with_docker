from django.urls import path
from .views import ItemDetailView
from .views import ItemListView
from .views import ItemEditView
from .views import ItemListByFavoriteView
from .views import ItemUserListView, ItemSearchView
from .views import ItemFavoriteView, ItemDeactivateView
from .views import ItemCategoryListView
from .views import ItemCategoryLocalListView
from .views import ItemCreateViewKaizen
from .views import ItemFavoriteViewKaizen



app_name = "items"
urlpatterns = [
    path('create2/', ItemCreateViewKaizen.as_view(), name='item_create2'),
    path('<int:pk>/delete/', ItemDeactivateView.as_view(), name="item_deactivate"),
    path('list/', ItemListView.as_view(), name='item_list'),
    path("items/category/<int:pk>/items/list/", ItemCategoryListView.as_view(), name="ItemCategoryListView" ),
    path("items/category/<int:pk>/items/list/local/", ItemCategoryLocalListView.as_view(), name="ItemCategoryLocalListView" ),
    path('list_u/',  ItemUserListView.as_view(), name='itemuser_list'),
    path('user/favorite/', ItemListByFavoriteView.as_view(), name='item_list_by_favorite'),
    path('search/', ItemSearchView.as_view(), name='item_search'),
    #path('mylist', MyItemListView.as_view(), name='item_mylist'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),    
    #axiosに変更 path('item/<int:pk>/favorite/', ItemFavoriteView.as_view(), name='item_favorite'),
    path('item/<int:pk>/favorite/', ItemFavoriteViewKaizen.as_view(), name='item_favorite'),
    path('<int:pk>/edit/', ItemEditView.as_view(), name='item_edit'),    
]

