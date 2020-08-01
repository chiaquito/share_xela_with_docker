from config.constants import ContextKey
from config.utils     import paginate_queryset
from django.shortcuts import render, redirect
from django.views.generic import View
from items.models import Item
# Create your views here.


class MyItemListView(View):
	def get(self, request, *args, **kwargs):
		context = {}
		#ユーザー認証されていないときは、ログインページにつなぐ
		if request.user.is_anonymous == True:
			return redirect('account_login')
			#return render(request, 'config/signup.html', context)

		#自分が作成した記事を表示する
		item_objects = Item.objects.filter(user=request.user).order_by("-created_at").filter(active=True)
		page_obj = paginate_queryset(request, item_objects)

		if item_objects.count() > 0:
			context[ ContextKey.ITEM_OBJECTS ] = page_obj.object_list
			context[ ContextKey.PAGE_OBJ ] = page_obj
			return render(request, "items/list_items.html", context)
		else:
			return render(request, "mypages/no_items.html", context)


