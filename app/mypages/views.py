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
		item_objects = Item.objects.filter(user=request.user).order_by("-created_at")
		if item_objects.count() > 0:
			context["item_objects"] = item_objects
			return render(request, "items/list_items.html", context)
		else:
			return render(request, "mypages/no_items.html", context)


