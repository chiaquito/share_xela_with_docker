from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View, DeleteView
from django.views.generic import CreateView
from django.db.models import Avg, Sum
from django.http import HttpResponse, JsonResponse
from config.constants import TemplateKey, TemplateName
from config.constants import ContextKey
from config.constants import ViewName
from items.models import Item
from items.forms import ItemModelForm
from items.forms import ItemFirstModelForm
from items.utils import addBtnFavToContext
from item_contacts.forms import ItemContactModelForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from favorite.models            import Favorite
from categories.models          import Category
from item_contacts.models       import ItemContact
from profiles.models            import Profile
from solicitudes.models         import Solicitud
from direct_messages.models     import DirectMessage
from django.db.models import Q

# Create your views here.




class ItemListView(View):
	def get(self, request, *args, **kwargs):

		context = {}
		item_objects = Item.objects.all()
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)



class ItemListByFavoriteView(View):
	def get(self, request, *args, **kwargs):
		"""機能
		認証したユーザーのfavボタンを押したアイテムを一覧表示する

		endpoint: 'items/user/favorite/'
		name: 'items:item_list_by_favorite'
		"""

		#アクセスユーザーの制限
		if request.user.is_anonymous:
			return redirect(ViewName.HOME)

		#表示するデータを取得
		context = {}
		request_user = User.objects.get(username=request.user.username)
		item_objects = Item.objects.filter(favorite_users=request_user)
		context[ContextKey.ITEM_OBJECTS] = item_objects
		return render(request, TemplateName.ITEM_LIST, context)







class ItemUserListView(View):
	"""
	usernameアンカーからuserの投稿記事をリスト表示する。
	sessionを使って表示する仕組みを用いる。
	"""
	def get(self, request, *args, **kwargs):
		context = {}

		user_obj = request.session["user_obj"]
		#print(user_obj)
		item_objects = Item.objects.filter(user=user_obj).order_by("-created_at")
		context['user_obj'] = user_obj
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)







class ItemCategoryListView(View):

	def get(self, request, *args, **kwargs):
		"""機能

		endpoint: 'items/category/<int:pk>/items/list/'
		name: ItemCategoryListView
		"""
		"""テスト項目
		"""
		category_number = self.kwargs["pk"]

		if category_number == 999:
			return redirect('item:item_list')

		item_objects = Item.objects.filter(category__number=category_number).filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, "items/no_item.html")
		else:
			print(item_objects.count())
			context = {}
			context[ ContextKey.ITEM_OBJECTS ] = item_objects
			return render(request, TemplateKey.ITEM_LIST, context)





class ItemCategoryLocalListView(View):
	#dar,venderを一覧するView
	# このAPIViewを発行するときはクライアントは必ずユーザー認証が終わっているので、ユーザー認証等は考える必要ない。

	def get(self, request, *args, **kwargs):
		"""機能

		endpoint: 'items/category/<int:pk>/items/list/local/'
		name: -
		"""
		"""テスト項目
		"""


		context = {}
		#ユーザー認証なされていないときはユーザーログインページに飛ばす
		if request.user.is_anonymous == True :
			return redirect("account_login")
		elif Profile.objects.filter(user=request.user).count() == 0:
			return redirect("account_login")
		profile_obj = Profile.objects.get(user=request.user)


		category_number = self.kwargs["pk"]
		if category_number == 999:
			return redirect('item:item_list')

		#categoryObj = Category.objects.get(number=category_number)
		item_objects = Item.objects.filter(category__number=category_number).filter(adm1=profile_obj.adm1).exclude(active=False).order_by("-created_at")
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)		





class ItemDarListView(View):
	"""
	グアテマラのすべてのdonar vender投稿を表示させる
	category:1 "Gente que quiere donar o vender"
	endpoint: "items/list_dt/"
	name: "items:itemdar_list"
	"""
	"""テスト項目
	記事がないときはitems_no_item.htmlテンプレートが使用される

	"""

	def get(self,request, *args, **kwargs):
		
		#ca_obj = Category.objects.get(name="1")
		#print(dir(ca_obj))
		#print(ca_obj.name)
		#print(ca_obj.get_name_display())
		#print(dir(ca_obj.serializable_value))
		item_objects = Item.objects.filter(category__number="1").filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, "items/no_item.html")

		else:
			print(item_objects.count())
			context = {}
			context[ ContextKey.ITEM_OBJECTS ] = item_objects
			return render(request, TemplateKey.ITEM_LIST, context)



#class ItemDarPrefecturaListView(View):
class ItemDarLocalListView(View):
	"""
	profileのadm1と同じ属性のアイテムのみを表示させる

	#記事がないときはno_item.htmlを表示する
	#ユーザー認証なされていないときはユーザーログインページに飛ばす

	"""
	def get(self, request, *args, **kwargs):
		context = {}
		#ユーザー認証なされていないときはユーザーログインページに飛ばす
		if request.user.is_anonymous == True :
			return redirect("account_login")
		elif Profile.objects.filter(user=request.user).count() == 0:
		 	return redirect("account_login")
		profile_obj = Profile.objects.get(user=request.user)
		item_objects = Item.objects.filter(category__number="1").filter(adm1=profile_obj.adm1).filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)		



class ItemQuererListView(View):
	"""
	グアテマラのすべてのquerer投稿を表示させる
	"""
	def get(self,request, *args, **kwargs):
		item_objects = Item.objects.filter(category__number="2").filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)
		context = {}
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)



class ItemQuererPrefecutraListView(View):
	"""
	quererカテゴリのうちadm1と一致した投稿を表示させる
	"""
	def get(self,request, *args, **kwargs):
		
		if request.user.is_anonymous == True :
			return redirect('account_login')
		elif Profile.objects.filter(user=request.user).count() == 0:
		 	return redirect("account_login")
		profile_obj = Profile.objects.get(user=request.user)
		item_objects = Item.objects.filter(category__number="2").filter(adm1=profile_obj.adm1).filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)
		context = {}		
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)





class ItemAnuncioListView(View):
	"""
	グアテマラのすべてのanuncio投稿を表示させる
	"""
	def get(self,request, *args, **kwargs):
		context = {}
		#category_obj = Category.objects.get(name="Anunciate")
		#print(category_obj)
		item_objects = Item.objects.filter(category__number="3").filter(active=True).order_by("-created_at")
		#print(item_objects.count())
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)
			
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)




class ItemAnuncioPrefecturaListView(View):
	"""
	profileのadm1と同じ属性のアイテムのみを表示させる

	#記事がないときはno_item.htmlを表示する
	#ユーザー認証なされていないときはユーザーログインページに飛ばす
	後日実装する。profileオブジェがない時は作成させるページに持っていく。
	"""
	def get(self, request, *args, **kwargs):
		context = {}
		#ユーザー認証なされていないときはユーザーログインページに飛ばす
		if request.user.is_anonymous == True :
			return redirect("account_login")
		elif Profile.objects.filter(user=request.user).count() == 0:
		 	return redirect("account_login")
		profile_obj = Profile.objects.get(user=request.user)
		#category_obj = Category.objects.get(name="Anunciate")
		item_objects = Item.objects.filter(category__number="3").filter(adm1=profile_obj.adm1).filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)




class ItemBuscarHabitacionListView(View):
	"""機能
	endpoint: /items/list_bh/
	name: "items:BuscarHabitacionList"
	"""
	"""テスト項目
	category__name="4"が部屋を探している人達になっているか
	"""
	def get(self, request, *args, **kwargs):
		item_objects = Item.objects.filter(category__number="4").filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)

		context = {}
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)



class ItemBuscarHabitacionLocalListView(View):
	"""機能
	endpoint: /items/list_bh_local/
	name: "items:BuscarHabitacionLocalList"
	"""
	"""テスト項目
	"""
	def get(self, request, *args, **kwargs):
		
		#ユーザー認証なされていないときはユーザーログインページに飛ばす
		if request.user.is_anonymous == True :
			return redirect("account_login")
		elif Profile.objects.filter(user=request.user).exist() == False:
		 	return redirect("account_login")
		profile_obj = Profile.objects.get(user=request.user)
		item_objects = Item.objects.filter(category__number="4").filter(adm1=profile_obj.adm1).filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)
		context = {}
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)




class ItemAlquilarHabitacionListView(View):
	"""機能
	endpoint: /items/list/ah/
	name: "items:AlquilarHabitacionList"
	"""
	"""テスト項目
	category__name="5"が部屋を貸したい人達になっているか
	"""
	def get(self, request, *args, **kwargs):
		item_objects = Item.objects.filter(category__number="5").filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)

		context = {}
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)




class ItemAlquilarHabitacionLocalListView(View):
	"""機能
	endpoint: /items/list/ah_local/
	name: "items:AlquilarHabitacionLocalList"
	"""
	"""テスト項目
	"""
	def get(self, request, *args, **kwargs):
		
		#ユーザー認証なされていないときはユーザーログインページに飛ばす
		if request.user.is_anonymous == True :
			return redirect("account_login")
		elif Profile.objects.filter(user=request.user).exist() == False:
		 	return redirect("account_login")
		profile_obj = Profile.objects.get(user=request.user)
		item_objects = Item.objects.filter(category__number="5").filter(adm1=profile_obj.adm1).filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)
		context = {}
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)




class ItemBuscarTrabajoListView(View):
	"""機能
	endpoint: "items/list/bt/"
	name: "items:BuscarTrabajoList"
	"""
	"""テスト項目
	category__name="6"が仕事を探している人達になっているか
	"""
	def get(self, request, *args, **kwargs):
		item_objects = Item.objects.filter(category__number="6").filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)

		context = {}
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)




class ItemBuscarTrabajoLocalListView(View):
	"""機能
	endpoint: "items/list/bt_local/"
	name: "items:BuscarTrabajoLocalList"
	"""
	"""テスト項目
	"""
	def get(self, request, *args, **kwargs):
		
		#ユーザー認証なされていないときはユーザーログインページに飛ばす
		if request.user.is_anonymous == True :
			return redirect("account_login")
		elif Profile.objects.filter(user=request.user).exist() == False:
		 	return redirect("account_login")
		profile_obj = Profile.objects.get(user=request.user)
		item_objects = Item.objects.filter(category__number="6").filter(adm1=profile_obj.adm1).filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)
		context = {}
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)




class ItemBuscarTrabajadorListView(View):
	"""機能
	endpoint: items/list/btr/
	name: "items:BuscarTrabajadorList"
	"""
	"""テスト項目
	category__name="6"が仕事を探している人達になっているか
	"""
	def get(self, request, *args, **kwargs):
		item_objects = Item.objects.filter(category__number="7").filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)

		context = {}
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)




class ItemBuscarTrabajadorLocalListView(View):
	"""機能
	endpoint: items/list/btr_local/
	name: "items:BuscarTrabajadorLocalList"
	"""
	"""テスト項目
	"""
	def get(self, request, *args, **kwargs):
		
		#ユーザー認証なされていないときはユーザーログインページに飛ばす
		if request.user.is_anonymous == True :
			return redirect("account_login")
		elif Profile.objects.filter(user=request.user).exist() == False:
		 	return redirect("account_login")
		profile_obj = Profile.objects.get(user=request.user)
		item_objects = Item.objects.filter(category__number="7").filter(adm1=profile_obj.adm1).filter(active=True).order_by("-created_at")
		#記事がないときはno_item.htmlを表示する
		if item_objects.count() == 0:
			return render(request, TemplateKey.NO_ITEMS)
		context = {}
		context[ ContextKey.ITEM_OBJECTS ] = item_objects
		return render(request, TemplateKey.ITEM_LIST, context)










class ItemDetailView(View):
	"""機能
	出品物の詳細ページを表現するview
	出品物に対するメッセージも表示する
	出品者のプロフィールも表示する
	また、postメソッドでは、メッセージを投稿できる
	"""

	def get(self, request, *args, **kwargs):
		"""
		endpoint: items/<int:pk>/
		"""

		context = {}
		pk = self.kwargs["pk"]
		item_obj = Item.objects.get(id=pk)
		#user_obj = User.objects.get(username=item_obj.user)
		user_obj = item_obj.user
		#なんのためのセッションか忘れてしまった。
		self.request.session["user_obj"] = user_obj
		profile_obj = Profile.objects.get(user=user_obj)
		solicitudes_objects     = item_obj.solicitudes.all()
		item_contact_objects    = item_obj.item_contacts.all().order_by('-timestamp')
		direct_messages_objects = DirectMessage.objects.filter(item=item_obj)

		"""
		#ココリファクタリングの余地あり
		if item_obj.direct_message != None:
			direct_messages_objects = item_obj.direct_message.direct_message_contents.all()
		else:
			direct_messages_objects = DirectMessage.objects.filter(item=item_obj)
		"""



		# 共通contextを設定
		context["item_obj"] = item_obj
		context["profile_obj"] = profile_obj
		context["solicitudes_objects"] = solicitudes_objects
		context["item_contact_objects"] = item_contact_objects
		context["direct_messages_objects"] = direct_messages_objects



		# context["btn_fav"]を設定
		context = addBtnFavToContext(request, item_obj ,context)



		# context["btn_choice"]を設定

		#ユーザーが未認証の場合 ->ボタン情報をcontextに追加しない
		if request.user.is_anonymous:
			pass

		#ユーザーが投稿主かつ申請者なしの場合 -> 申請者を選ぶボタンを表示しない
		elif request.user == user_obj and solicitudes_objects.count() == 0:
			btn_choice = "no_solicitudes"
			context["btn_choice"] = btn_choice

		#ユーザーが投稿主かつ申請者有＆取引相手未決定の場合 -> ”申請者を選ぶボタン”を表示させる。
		elif request.user == user_obj and solicitudes_objects.count() != 0 and direct_messages_objects.count() == 0:
			btn_choice = "select_solicitudes"
			context["btn_choice"] = btn_choice

		#ユーザーが投稿主かつ取引相手決定済みの場合 -> ”取引画面へ映るボタン”を表示させる。
		elif request.user == user_obj and direct_messages_objects.count() != 0:
			btn_choice = 'torihiki'
			context["btn_choice"] = btn_choice

		#ユーザーが投稿主以外かつ未申請の場合 -> ”申し込むボタン”を表示させる。
		elif request.user != user_obj and solicitudes_objects.filter(applicant=Profile.objects.get(user=request.user)).count() == 0 and direct_messages_objects.filter(item=item_obj).count() == 0:
			btn_choice = "moushikomi"
			context["btn_choice"] = btn_choice

		#ユーザーが投稿主以外かつ申請済みの場合 -> ”申請済みのdisabledボタン”を表示させる。
		elif request.user != user_obj and solicitudes_objects.filter(applicant=Profile.objects.get(user=request.user)).count() != 0 and direct_messages_objects.count() == 0:
			btn_choice = 'sumi'
			context["btn_choice"] = btn_choice

		#ユーザーが投稿主以外かつ自分に決定の場合 -> ”取引画面に移るボタン”を表示させる
		elif request.user != user_obj and direct_messages_objects.filter(participant=Profile.objects.get(user=request.user)).count() == 1:
			btn_choice = 'torihiki'
			context["btn_choice"] = btn_choice

		#ユーザーが投稿主以外かつ他者に決定の場合 -> ”このアイテムは他者に決定しましたのdisabledボタン”を表示させる。
		elif request.user != user_obj and direct_messages_objects.filter(participant=Profile.objects.get(user=request.user)).count() == 0:
			btn_choice = 'fail'
			context["btn_choice"] = btn_choice

		# 記事作成者のフィードバックに関する["feedback_sum"]["feedback_ave"]
		feedback_sum = profile_obj.feedback.all().aggregate(Sum('level'))['level__sum']
		context["feedback_sum"] = feedback_sum
		feedback_ave = profile_obj.feedback.all().aggregate(Avg('level'))['level__avg']
		context["feedback_ave"] = feedback_ave





		# コメントを記入するための context["form"]を設定

		#ユーザーが未認証の場合 ->
		if request.user.is_anonymous:
			data = {"post_user":request.user, "item":item_obj }
			form = ItemContactModelForm(initial=data)
			context["form"] = form

		#ユーザーが投稿主の場合 -> 投稿記事主以外のitem_contactオブジェクトを取得し、各プロフィールオブジェクトをreply_userにセットする
		elif request.user == user_obj:
			profile_obj = Profile.objects.get(user=request.user)
			data = {"post_user":profile_obj , "item":item_obj}
			form = ItemContactModelForm(initial=data)
			context["form"]	= form

		#ユーザーが投稿主の場合 -> 投稿記事主以外のitem_contactオブジェクトを取得し、各プロフィールオブジェクトをreply_userにセットする
		elif request.user != user_obj and Profile.objects.filter(user=request.user).count() != 0:
			profile_obj = Profile.objects.get(user=request.user)
			data = {"post_user":profile_obj, "item":item_obj }
			form = ItemContactModelForm(initial=data)
			context["form"] = form




		# context["dm-obj"]を設定 (try exceptで書き換えられる)
		if request.user.is_anonymous:
			pass

		elif request.user == user_obj and direct_messages_objects.count() != 0:
			dm_obj = DirectMessage.objects.get(item=item_obj)
			context["dm_obj"] = dm_obj

		elif request.user != user_obj and direct_messages_objects.filter(participant=Profile.objects.get(user=request.user)).count() != 0:
			dm_obj = DirectMessage.objects.get(item=item_obj)
			context["dm_obj"] = dm_obj


		#テンプレートレンダリング
		if request.user.is_anonymous:
			return render(request, TemplateKey.ITEM_DETAIL, context)

		elif request.user == user_obj :
			return render(request, TemplateKey.ITEM_DETAIL, context)

		#おそらく以下のロジックは通らないと思われる。(安全の為)
		elif request.user != user_obj and Profile.objects.filter(user=request.user).count() == 0:
			return redirect('profiles:profile_creating')

		elif request.user != user_obj :
			return render(request, TemplateKey.ITEM_DETAIL, context)







class ItemEditView(View):

	def get(self, request, *args, **kwargs):
		"""機能

		endpoint: "items/<int:pk>/edit/"
		name: "items:'item_edit'"
		"""

		#アクセス制限(未認証ユーザー)
		if request.user.is_anonymous:
			return redirect(ViewName.HOME)

		pk = self.kwargs["pk"]
		item_obj = Item.objects.get(id=pk)

		#アクセス制限(記事作成者以外のアクセス)
		if item_obj.user != request.user:
			return redirect(ViewName.HOME)
		print(item_obj.adm1)
		print(item_obj.adm2)

		data = {
			"category" : item_obj.category,
			"title" : item_obj.title,
			"description" : item_obj.description,
			"adm0" : item_obj.adm0,
			#"adm1" : item_obj.adm1,
			#"adm2" : item_obj.adm2,
			"image1" : item_obj.image1,
			"image2" : item_obj.image2,
			"image3" : item_obj.image3,
			#"image4" : item_obj.image4,
			#"image5" : item_obj.image5,
			#"image6" : item_obj.image6,
			'price': item_obj.price,
			#'point': item_obj.point,
			#"radius": item_obj.radius
			}

		form = ItemModelForm(data, initial=data)
		context = {}
		context["form"] = form
		context["item_obj"] = item_obj
		context["title"] = "Editar Articulo"
		return render(request, "items/create_item_k.html", context)


	def post(self, request, *args, **kwargs):
		"""
		画像が追加された場合と追加されない場合で対応できないとこまる
		"""
		context = {}
		pk = self.kwargs["pk"]
		item_obj = Item.objects.get(id=pk)
		form = ItemModelForm(request.POST, request.FILES)
		if form.is_valid() == True:

			
			title       = form.cleaned_data["title"]
			#user        = form.cleaned_data["user"]
			description =  form.cleaned_data["description"]
			#item_obj.user = request.user			
			item_obj.title = title
			item_obj.description = description
			
			adm1 = request.POST["adm1"]
			adm2 = request.POST["adm2"]
			obj.adm1 = adm1
			obj.adm2 = adm2	
					
			try:
				wkt = request.POST["point"]
				point = GEOSGeometry(wkt)
				obj.point = point 
			except:
				pass
			try:
				obj.radius = int(request.POST["radius"])
			except:
				pass

			try:
				item_obj.image1 = request.FILES['image1']
			except:
				pass
			try:
				item_obj.image2 = request.FILES['image2']
			except:
				pass
			try:
				item_obj.image3 = request.FILES['image3']
			except:
				pass
			item_obj.save()
			context["item_obj"] = item_obj
			print("IS_VALID == TRUE")

			return render(request, "items/edited.html", context)

		elif form.is_valid() == False:
			print("IS_VALID == FALSE")
			return redirect('items:item_edit')



class ItemDeactivateView(View):

	def get(self, request, *args, **kwargs):
		context = {}
		pk = self.kwargs["pk"]
		item_obj = Item.objects.get(id=pk)
		context["item_obj"] = item_obj
		return render(request, "items/confirm_delete.html", context)


	def post(self, request, *args, **kwargs):
		context = {}
		pk = self.kwargs["pk"]
		item_obj = Item.objects.get(id=pk)
		item_obj.active = False
		item_obj.save()
		return render(request, "items/deleted.html", context)



'''
class ItemCreateView(View):
	"""
	Hacer Alticulosボタンを押した時発動する
	"""

	def get(self, request, *args, **kwargs):
		context = {}
		#{ ユーザー認証されていないときは、ログインページにつなぐ }
		if request.user.is_anonymous == True:
			return redirect('account_login')
			
		profile_obj_count = Profile.objects.filter(user=request.user).count()
		#{ user認証されているけどまだprofileオブジェクトがない場合は、profileオブジェクトの作成ページにつなぐ }
		if profile_obj_count == 0:
			self.request.session["hacer_articulos"] = True
			return redirect('profiles:profile_creating')


		#{ profile:profile_settingからリダイレクトされた場合には、追加でメッセージを表示する }
		# session "hacer_articulos"
		if "hacer_articulos" in self.request.session.keys():
			messages.info(request, 'プロフィール設定ができました。投稿してください。')
			del self.request.session["hacer_articulos"]


		profile_obj = Profile.objects.get(user=request.user)
		data = { 
		"price": 0,
		#"user": profile_obj.user,
		"adm0": profile_obj.adm0,
		"adm1": profile_obj.adm1,
		"adm2": profile_obj.adm2,
		}
		form = ItemModelForm(data, initial=data)
		#form = ItemModelForm()
		context["form"] = form

		return render(request, 'items/create_item.html', context)



	def post(self, request, *args, **kwargs):
		"""
		endpoint:"items/'create/"
		name: "items:item_create"
		"""
		"""テスト項目
		categoryを選択しない場合にはItemオブジェクトが作られない
		"""


		print(request.POST)

		form = ItemModelForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			try:
				obj.image1 = request.FILES['image1']
			except:
				pass
			try:
				obj.image2 = request.FILES['image2']
			except:
				pass
			try:
				obj.image3 = request.FILES['image3']
			except:
				pass
			try:	
				obj.image4 = request.FILES['image4']
			except:
				pass
			try:
				obj.image5 = request.FILES['image5']
			except:
				pass
			try:
				obj.image6 = request.FILES['image6']
			except:
				pass
			obj.user = request.user
			obj.save()

			context = {}
			context["item_obj"] = obj
			#request.session["articulos_id"] = obj.id
			return render(request, 'items/created.html', context)

		else:
			for error in form.errors:
				print(error)
			
			context = {}
			context["form"] = form
			return render(request, 'items/create_item.html', context)

'''

#from prefecturas.list_data import DEPARTAMENTO_CHOICES
#import json



from django.contrib.gis.geos import GEOSGeometry

class ItemCreateViewKaizen(View):
	"""
	Hacer Alticulosボタンを押した時発動する
	"""

	def get(self, request, *args, **kwargs):
		context = {}
		#{ ユーザー認証されていないときは、ログインページにつなぐ }
		if request.user.is_anonymous == True:
			return redirect('account_login')
			
		profile_obj_count = Profile.objects.filter(user=request.user).count()
		#{ user認証されているけどまだprofileオブジェクトがない場合は、profileオブジェクトの作成ページにつなぐ }
		if profile_obj_count == 0:
			self.request.session["hacer_articulos"] = True
			return redirect('profiles:profile_creating')


		#{ profile:profile_settingからリダイレクトされた場合には、追加でメッセージを表示する }
		# session "hacer_articulos"
		if "hacer_articulos" in self.request.session.keys():
			messages.info(request, 'プロフィール設定ができました。投稿してください。')
			del self.request.session["hacer_articulos"]


		profile_obj = Profile.objects.get(user=request.user)
		data = { 
		"price": 0,
		#"user": profile_obj.user,
		"adm0": profile_obj.adm0,
		"adm1": profile_obj.adm1,
		"adm2": profile_obj.adm2,
		}
		form = ItemModelForm(data, initial=data)
		#form = ItemModelForm()
		context["form"] = form
		context["title"] = "Crear Articulo"

		return render(request, 'items/create_item_k.html', context)



	def post(self, request, *args, **kwargs):
		"""
		endpoint:"items/'create_k/"
		name: "items:item_create2"
		"""
		"""テスト項目
		categoryを選択しない場合にはItemオブジェクトが作られない
		"""


		print(request.POST)

		form = ItemModelForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			adm1 = request.POST["adm1"]
			adm2 = request.POST["adm2"]
			obj.adm1 = adm1
			obj.adm2 = adm2
			obj.save()

			try:
				wkt = request.POST["point"]
				point = GEOSGeometry(wkt)
				obj.point = point 
			except:
				pass
			try:
				obj.radius = int(request.POST["radius"])
			except:
				pass
			try:
				obj.image1 = request.FILES['image1']
			except:
				pass
			try:
				obj.image2 = request.FILES['image2']
			except:
				pass
			try:
				obj.image3 = request.FILES['image3']
			except:
				pass
			#try:	
			#	obj.image4 = request.FILES['image4']
			#except:
			#	pass
			#try:
			#	obj.image5 = request.FILES['image5']
			#except:
			#	pass
			#try:
			#	obj.image6 = request.FILES['image6']
			#except:
			#	pass
			obj.user = request.user
			obj.save()

			context = {}
			context["item_obj"] = obj
			#request.session["articulos_id"] = obj.id
			return render(request, 'items/created.html', context)

		else:
			for error in form.errors:
				print(error)
			
			context = {}
			context["form"] = form
			return render(request, 'items/create_item_k.html', context)	





class ItemSearchView(View):
	"""
	インプットフォームに入力されたキーをもとにarticulos(item)を
	リスト化し、リスト表示する

	"""
	def get(self, request, *args, **kwargs):
		
		context = {}
		#print(dir(self.request))
		if self.request.method == "GET":
			#print(self.request.GET)
			q = self.request.GET.get("q")
			#print(q)
			#title_query = Item.objects.filter(title__icontains=q)
			#description_query = Item.objects.filter(description__icontains=q)
			item_objects = Item.objects.filter(Q(title__icontains=q)|Q(description__icontains=q))
			context["item_objects"] = item_objects

			return render(request, TemplateKey.ITEM_LIST, context)




class ItemFavoriteView(View):

	def post(self, request, *args, **kwargs):
		"""
		endpoint: 'items/item/<int:pk>/favorite/'
		name: 'items:item_favorite'

		このViewを通るのはすべて認証ユーザーである。
		なぜならFavボタンを表示する対象は認証ユーザーのみであるからだ。

		ただし、urlを変更することでアクセスするユーザーの可能性も考えられるのでanonymousははじく。

		コレに関しては、AJAXを使う改善点が挙げられる。優先度は低い。
		"""
		fav_obj_id = None
		pk = self.kwargs["pk"]


		if request.user.is_anonymous:
			return redirect(ViewName.ITEM_DETAIL, pk)   #テスト実施項目:非認証ユーザーのアクセスはリダイレクトされるか?　リダイレクトされる場所はアイテム詳細ページか？ 同じidのアイテムページにリダイレクト？
		
		item_obj = Item.objects.get(id=pk)
		user_obj = User.objects.get(username=request.user.username)

		# item_obj.favorite_usersに追加する
		if user_obj not in item_obj.favorite_users.all():
			item_obj.favorite_users.add(user_obj)

		elif user_obj in item_obj.favorite_users.all():
			item_obj.favorite_users.remove(user_obj)

		return redirect(ViewName.ITEM_DETAIL, item_obj.id)





class ItemFavoriteViewKaizen(View):
	
	def post(self, request, *args, **kwargs):
		"""
		endpoint: 'items/item/<int:pk>/favorite/'
		name: 'items:item_favorite'

		このViewを通るのはすべて認証ユーザーである。
		なぜならFavボタンを表示する対象は認証ユーザーのみであるからだ。

		ただし、urlを変更することでアクセスするユーザーの可能性も考えられるのでanonymousははじく。

		コレに関しては、AJAXを使う改善点が挙げられる。優先度は低い。
		""" 
		
		fav_obj_id = None
		pk = self.kwargs["pk"]


		if request.user.is_anonymous:
			return JsonResponse({"result":"no_change"})   #テスト実施項目:非認証ユーザーのアクセスはリダイレクトされるか?　リダイレクトされる場所はアイテム詳細ページか？ 同じidのアイテムページにリダイレクト？
		
		item_obj = Item.objects.get(id=pk)
		user_obj = User.objects.get(username=request.user.username)

		# item_obj.favorite_usersに追加する
		if user_obj not in item_obj.favorite_users.all():
			item_obj.favorite_users.add(user_obj)
			data = {"result": "added"}

		elif user_obj in item_obj.favorite_users.all():
			item_obj.favorite_users.remove(user_obj)
			data = {"result": "removed"}
		

		return JsonResponse(data)


