from django.shortcuts import render, redirect
from django.views.generic import View
from categories.models import Category
from avisos.models import Aviso
from profiles.models import Profile
from items.models import Item
from django.db.models import Q

from .forms import UsernameChangeForm, EmailAddressChangeForm
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib import messages
from api.constants import SerializerContextKey
from .constants import TemplateName





class HomeView(View):
	def get(self, request, *args, **kwargs):
		"""
		非ログインユーザーの場合、ログインかつプロフィールオブジェクトがある場合、ログインかつプロフィールオブジェクトがない場合に
		分けている
        endpoint:''
        name: 'home'
		"""
		
		context = {}
		if request.user.is_anonymous == True:
			return render(request, "config/home.html", context)

		elif request.user.is_authenticated == True and Profile.objects.filter(user=request.user).exists() == True :
			aviso_objects = Aviso.objects.filter(aviso_user=Profile.objects.get(user=request.user)).filter(checked=False)
			context["aviso_objects"] = aviso_objects
			context["aviso_count"] = aviso_objects.count()
			return render(request, "config/home.html", context)

		elif request.user.is_authenticated == True and Profile.objects.filter(user=request.user).exists() == False :
			return render(request, "config/home.html")


class HomeKaizenView(View):


    def get(self, request, *args, **kwargs):
        """
        非ログインユーザーの場合、ログインかつプロフィールオブジェクトがある場合、ログインかつプロフィールオブジェクトがない場合に
        分けている
        endpoint:''
        name: 'home'
        """

        item_objects_cosas = Item.objects.filter(Q(category__number="1")|Q(category__number="2")|Q(category__number="3")).exclude(active=False).order_by("-id")[:4]
        item_objects_habitacion = Item.objects.filter(Q(category__number="4")|Q(category__number="5")|Q(category__number="6")|Q(category__number="7")).exclude(active=False).order_by("-id")[:4]
        item_objects_trabajo = Item.objects.filter(Q(category__number="8")|Q(category__number="9")).exclude(active=False).order_by("-id")[:4]
        item_objects_tienda = Item.objects.filter(category__number="10").exclude(active=False).order_by("-id")[:4]        
        
        context = {}
        context[SerializerContextKey.ITEM_OBJECTS_COSAS]      = item_objects_cosas
        context[SerializerContextKey.ITEM_OBJECTS_HABITACION] = item_objects_habitacion
        context[SerializerContextKey.ITEM_OBJECTS_TRABAJO]    = item_objects_trabajo
        context[SerializerContextKey.ITEM_OBJECTS_TIENDA]     = item_objects_tienda

        if request.user.is_anonymous == True:
            return render(request, TemplateName.HOME, context)

        elif request.user.is_authenticated == True and Profile.objects.filter(user=request.user).exists() == True :
            aviso_objects = Aviso.objects.filter(aviso_user=Profile.objects.get(user=request.user)).filter(checked=False)
            context["aviso_objects"] = aviso_objects
            context["aviso_count"] = aviso_objects.count()
            return render(request, TemplateName.HOME, context)

        elif request.user.is_authenticated == True and Profile.objects.filter(user=request.user).exists() == False :
            return render(request, TemplateName.HOME)






class HowtoView(View):
	def get(self, request, *args, **kwargs):
		"""
		非ログインユーザーの場合、ログインかつプロフィールオブジェクトがある場合、ログインかつプロフィールオブジェクトがない場合に
		分けている

        endpoint: howto/
        name:  "howto"
		"""

		context = {}
		if request.user.is_anonymous == True:

			return render(request, 'config/howto.html')
		elif request.user.is_authenticated == True and Profile.objects.filter(user=request.user).exists() == True:

			aviso_objects = Aviso.objects.filter(aviso_user=Profile.objects.get(user=request.user)).filter(checked=False)
			context["aviso_objects"] = aviso_objects	
			context["aviso_count"] = aviso_objects.count()
			return render(request, 'config/howto.html', context)

		elif request.user.is_authenticated == True and Profile.objects.filter(user=request.user).exists() == False :
			return render(request, 'config/howto.html')




class CheckProfileView(View):
	"""
	サインアップのリダイレクト先としてこちらのViewを通す
	まず、request.userのProfileオブジェクトが存在しているかをチェックする
	もし無いなら取引エリアのみのフォームを作る。
	あるようならhomeページにリダイレクトさせる。
	"""
	def get(self, request, *args, **kwargs):
		if Profile.objects.filter(user=request.user).exists() == True:
			return redirect('home')
		elif Profile.objects.filter(user=request.user).exists() == False:
			return redirect('profiles:profile_creating')






class PrivacyView(View):

	def get(self, request, *args, **kwargs):

		return render(request, 'config/privacy_es.html')



class UsernameChangeView(View):


	def get(self, request, *args, **kwargs):
		context = {}
		form = UsernameChangeForm()
		context["form"] = form
		return render(request, 'config/change_username.html', context)


	def post(self, request, *args, **kwargs):
		context = {}
		form = UsernameChangeForm(request.POST)
		#context["form"] = form
		if form.is_valid():
			username = form.cleaned_data["username"]
			#print(username)
			user_obj = User.objects.get(username=request.user.username)
			#print(user_obj)
			user_obj.username = username
			user_obj.save()
			#messages.info(request,"usernameを変更しました。")
			messages.info(request, "Nombre de usuario ha cambiado")
			return redirect('profiles:profile')
		else:
			context["form"] = form

			return render(request, 'config/change_username.html', context)



class EmailAddressChangeView(View):

    def get(self, request, *args, **kwargs):
        """機能
        
        endpoint: 'email_change/'
        name: "email_change"
        """
        context = {}
        form    = EmailAddressChangeForm()
        context["form"] = form
        return render(request, 'config/change_emailaddress.html', context)


    def post(self, request, *args, **kwargs):
        """機能

        endpoint: 'email_change/'
        name: "email_change"
        """
        context = {}
        form    = EmailAddressChangeForm(request.POST)
        if form.is_valid():
			
            email    = form.cleaned_data["email"]
            if User.objects.filter(email=email).exists() == False :
                user_obj = User.objects.get(username=request.user.username)
                user_obj.email = email
                user_obj.save()
                email_obj = EmailAddress.objects.get(user=user_obj)
                email_obj.email = email
                email_obj.save()
                messages.info(request, "Dirección de correo electrónico ha cambiado")
                return redirect('profiles:profile')
            
            if User.objects.filter(email=email).exists() == True :
                messages.info(request, "La dirección de correo electrónico ya está registrada.")
                #messages.info(request, "そのメールアドレスはすでに登録されています。")
                context["form"] = form
                return render(request, 'config/change_emailaddress.html', context)

        else:
            #print("FALSE")
            context["form"] = form
            return render(request, 'config/change_emailaddress.html', context)



from django.contrib.gis.geos import GEOSGeometry
from items.forms import ItemModelForm
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse



class ListMyDataView(APIView):
    def post(self, request, *args, **kwargs):
        """
        収集したデータを送信する
        endpoint:"listing/shuppin/"
        name: ""
        """
        """テスト項目

        """
        user = User.objects.get(email="chiaki.amazon@gmail.com")
        new_dict = request.data.copy()

        category = request.data["category_"] 
        cate_obj = Category.objects.get(number=category)
        new_dict["category"] = cate_obj.id
        new_dict["point"] = GEOSGeometry(request.data["point_"])
        new_dict["user"] = user 
        #print(request.data)
        #print(new_dict)

        title = request.data["title"]
        price = request.data["price"]
        if len(Item.objects.filter(title=title).filter(price=price)) >= 1:
            print("既に登録済み")
            return HttpResponse("登録済みなので登録しない")


        print(request.FILES)
        form = ItemModelForm(new_dict)
        #print(form.is_valid())
        #print([ele for ele in form.errors])
        if form.is_valid():
            obj   = form.save(commit=False)
            adm1 = request.POST["adm1"]
            adm2 = request.POST["adm2"]
            obj.adm1 = adm1
            obj.adm2 = adm2            
            obj.point = new_dict["point"]
            obj.radius = new_dict["radius"]
            obj.user = user
            try:
                obj.image1 = request.FILES["file0"]
            except:
                pass
            try:    
                obj.image2 = request.FILES["file1"]
            except:
                pass
            try:    
                obj.image3 = request.FILES["file2"]
            except:
                pass
            obj.save()
        return HttpResponse("Response")







