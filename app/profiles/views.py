from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.views.generic import View
from .models import Profile
from .forms  import ProfileForm
from .forms  import CreatingProfileForm
from items.models import Item

from .strings import warningSettingAreaMessage, successEditProfileMessage


REDIRECT_TO_HOME = 'home'


class CreatingProfileView(View):

	"""
	Hacer Articulosボタンを押したときで、profileオブジェクトがない場合にはこのクラスビューが発動する。
	プロフィール変更ページと共にメッセージを表示させる。
	ビューの内容はProfileViewと少し異なる

	"""
	def get(self, request, *args, **kwargs):
		context  = {}
		user_obj = User.objects.get(username=request.user)
		data = {'user':request.user,}
		form = CreatingProfileForm(data, initial=data)
		context["user_obj"] = user_obj
		context["form"] = form

		messages.info(request, warningSettingAreaMessage)
		return render(request, 'profiles/profile_creating.html',context)



	def post(self, request, *args, **kwargs):
		"""
		Departamento, Municipioのデータを登録し、Profileオブジェクトを生成する。
		"""
		context = {}
		form = CreatingProfileForm(request.POST)

		if Profile.objects.filter(user=request.user).exists() == True:
			return redirect('home')

		elif Profile.objects.filter(user=request.user).exists() == False and form.is_valid() == True:
			obj = form.save(commit=False)
			obj.save()
			return redirect('home')



		else:
				
			return redirect('profiles:profile_creating')





class ProfileView(View):
	"""
	Profileオブジェクトが無いのはそもそも可能性が低い
	なぜならUserオブジェクト生成時にシグナルでProfileオブジェクトが生成されるから


	プロフィールデータが有る場合とない場合
	ユーザーデータがある場合とない場合のパターンに分けられる

	ここのViewsはまずprofileオブジェクトが有るかないかを注意する
	なければprofileオブジェクトを新規作成する必要があるし、
	あればobjectを更新するフローに流す必要がある。
	で、ユーザーである場合はprofileページを見れる仕組みにしておく。
	またユーザーでなければ、そもそも表示されないフローを導入する。

	"""
	def get(self, request, *args, **kwargs):
		"""機能

		endpoint: 'my_account/'
		name: 'profiles:profile'
		"""
		"""テスト項目 済
		済 ユーザー認証されていないユーザーのアクセスにはログインページのリダイレクトが実行される
		済 ユーザー認証されていないユーザーのアクセスにはログインページのhtmlが表示される

		済 認証済みユーザーのアクセスであるが、Profileオブジェクトがない場合には'profiles/profile.html'が使用される
		済 認証済みユーザーのアクセスであるが、Profileオブジェクトがない場合にはcontextに"user_obj"キーが存在する
		済 認証済みユーザーのアクセスであるが、Profileオブジェクトがない場合にはcontextに"form"キーが存在する
		済 認証済みユーザーのアクセスであるが、Profileオブジェクトがない場合の"form"はProfileFormクラスである
		済 認証済みユーザーのアクセスであるが、Profileオブジェクトがない場合にはcontextに"profile_obj"キーが存在しない

		済 認証済みユーザーのアクセスの場合contextに"profile_obj"キーが存在する
		済 認証済みユーザーのアクセスの場合contextに"user_obj"キーが存在する
		済 認証済みユーザーのアクセスの場合contextに"form"キーが存在する
		済 認証済みユーザーかつスーパーユーザ以外のアクセスの場合contextに"email_obj"キーが存在する

		"""

		context = {}


		#ユーザーアクセス制限
		if request.user.is_anonymous == True :
			return redirect('account_login')


		#稀のケース：認証済みユーザーのProfileオブジェクトがない場合 -> フォームを表示させる
		elif request.user.is_authenticated == True and Profile.objects.filter(user=request.user).exists() == False :			
			
			#contextにデータ格納
			user_obj = User.objects.get(username=request.user)
			context["user_obj"] = user_obj

			data = {'user':request.user,}
			form = ProfileForm(data, initial=data)			
			context["form"] = form
			#データとテンプレートのレンダリング
			return render(request, 'profiles/profile.html',context)


		#contextにデータ格納
		profile_obj = Profile.objects.get(user=request.user)
		context["profile_obj"] = profile_obj

		user_obj = User.objects.get(username=request.user)
		context["user_obj"] = user_obj

		data = {'user':request.user,
				'adm0' : profile_obj.adm0,
				'adm1' : profile_obj.adm1,
				'adm2' : profile_obj.adm2,
				'birthday' : profile_obj.birthday,
				'image' : profile_obj.image,
				'phonenumber' : profile_obj.phonenumber
				}
		form = ProfileForm(data, initial=data)
		context["form"] = form
		

		if request.user.is_superuser != True:
			email_obj = EmailAddress.objects.get(user=user_obj)
			context["email_obj"] = email_obj
		
		
		#データとテンプレートのレンダリング
		return render(request, 'profiles/profile.html',context)




	def post(self, request, *args, **kwargs):
		"""
		入力されたフォームデータに基づいてprofileオブジェクトを生成する

		Hacer Articulosボタンでリダイレクトされたケースで
		新たにprofileオブジェクトを生成する場合には、生成後products:item_createにリダイレクトする

		"""
		context = {}
		form = ProfileForm(request.POST, request.FILES)

		if Profile.objects.filter(user=request.user).exists() == False :

			if form.is_valid():
				obj = form.save(commit=False)

				#画像が送信された場合画像データをprofileオブジェクトに登録する
				if "image" in request.FILES.keys():
					obj.image = request.FILES["image"]
				obj.save()
				#print(self.request.session.keys())
				if "hacer_articulos" in self.request.session :

					return redirect('items:item_create2')

				messages.info(request, successEditProfileMessage)
				return redirect('profiles:profile')

			else:
				#print("profiles 再トライ")
				return redirect('profiles:profile')




		elif Profile.objects.filter(user=request.user).exists() == True :

			if form.is_valid() == True:

				adm0 = form.cleaned_data["adm0"]
				adm1 = form.cleaned_data["adm1"]
				adm2 = form.cleaned_data["adm2"]
				birthday    = form.cleaned_data["birthday"]
				phonenumber = form.cleaned_data["phonenumber"]

				profile_obj = Profile.objects.get(user=request.user)

				profile_obj.adm0 = adm0
				profile_obj.adm1 = adm1
				profile_obj.adm2 = adm2
				profile_obj.birthday = birthday
				profile_obj.phonenumber = phonenumber

				#画像が送信された場合画像データをprofileオブジェクトに登録する
				if "image" in request.FILES.keys():
					profile_obj.image = request.FILES["image"]
				profile_obj.save()

				messages.info(request, successEditProfileMessage)
				return redirect('profiles:profile')
				
			else:
				return redirect('profiles:profile')





class ProfileShowToOthersView(View):
	"""
	html上のuserをクリックしたときに表示されるuser情報を表示する	
	記事作成者はユーザー認証しているのが前提で、ユーザ登録していることはほぼ100%Profileオブジェクトが生成されている。

	"""
	def get(self, request, *args, **kwargs):
		"""機能


		endpoint: "/profiles/user/<int:pk>/profile/"
		name: "profiles:profile_show"
		"""
		"""テスト項目
		済 記事作成者のProfileオブジェクトが存在する場合においてアクセスユーザーがアクセスする時にはprofiles/profile_for_others.htmlテンプレートが使われる
		済 記事作成者のProfileオブジェクトが存在する場合において記事作成者がアクセスする時にはprofiles/profile_for_others.htmlテンプレートが使われる
		済 記事作成者のProfileオブジェクトが存在する場合においてAnonymous_userがアクセスする時にはprofiles/profile_for_others.htmlテンプレートが使われる
		済 記事作成者のProfileオブジェクトが存在しない場合はhomeへリダイレクトが実行される
		済 記事作成者のProfileオブジェクトが存在しない場合はリダイレクトされ、home用のテンプレートが使用される
		"""
		context = {}
		user_obj_pk = self.kwargs["pk"]
		if Profile.objects.filter(user__id=user_obj_pk).exists():
			profile_obj = Profile.objects.get(user__id=user_obj_pk)
			context['profile_obj'] = profile_obj
			return render(request, 'profiles/profile_for_others.html', context)

		return redirect('home')



class ItemUserListView(View):
	"""
	usernameアンカーからuserの投稿記事をリスト表示する。
	sessionを使って表示する仕組みを用いる。
	"""
	def get(self, request, *args, **kwargs):
		context = {}

		user_obj = request.session["user_obj"]
		#print(user_obj)
		item_objects = Item.objects.filter(user=user_obj)
		context['user_obj'] = user_obj
		context["item_objects"] = item_objects
		return render(request, "items/list_items.html", context)




