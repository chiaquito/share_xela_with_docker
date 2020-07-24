from django.shortcuts import render, redirect
from django.views.generic import View
# Create your views here.
from item_contacts.models import ItemContact
from .models import Aviso

from items.models import Item
from profiles.models import Profile
from direct_messages.models import DirectMessageContent
from direct_messages.models import DirectMessage
from solicitudes.models import Solicitud
from item_contacts.models import ItemContact





class AvisosAllListView(View):

	def get(self, request, *args, **kwargs):
		"""
		endpoint: /avisos/all/
		name: "avisos:avisos_alllist"
		"""

		if request.user.is_anonymous == True:
			return redirect('account_login')

		elif Profile.objects.filter(user=request.user).exists() == False:
			return redirect('profiles:profile_creating')

		else:

			context = {}
			aviso_objects = Aviso.objects.filter(aviso_user=Profile.objects.get(user=request.user)).order_by("-created_at")
			aviso_count = Aviso.objects.filter(aviso_user=Profile.objects.get(user=request.user)).filter(checked=False).count()
			context["aviso_objects"] = aviso_objects
			context["aviso_count"] = aviso_count
			context["type"] = "ALL"
			return render(request, 'avisos/avisos_prototype.html',context)




class AvisosListView(View):

	def get(self, request, *args, **kwargs):

		if request.user.is_anonymous == True:
			return redirect('account_login')

		elif Profile.objects.filter(user=request.user).exists() == False:
			return redirect('profiles:profile_creating')

		else:

			context = {}
			aviso_objects = Aviso.objects.filter(aviso_user=Profile.objects.get(user=request.user)).filter(checked=False).order_by("-created_at")
			context["aviso_objects"] = aviso_objects
			context["aviso_count"] = aviso_objects.count()
			context["type"] = "FILETERED"
			#return render(request, 'avisos/avisos_prototype_filtered.html',context)
			return render(request, 'avisos/avisos_prototype.html',context)





class AvisoCheckingView(View):

	def get(self, request, *args, **kwargs):
		"""
		pkからavisoオブジェクトをgetで取り出す。
		取り出したオブジェクトのcheckedをTrueに変更する。
		objectに基づいて各avisoの詳細ページにリダイレクトをかける。
		"""
		pk = self.kwargs["pk"]
		aviso_obj = Aviso.objects.get(id=pk)
		aviso_obj.checked = True
		aviso_obj.save()

		#aviso_objがなんのモデルを擁しているかを判定し、リダイレクトをかける
		#directmessageかどうか

		print(aviso_obj.content_type.model)

		if aviso_obj.content_type.model == "directmessagecontent":

			pk = aviso_obj.object_id
			dmc_obj = DirectMessageContent.objects.get(id=pk)
			return redirect('direct_messages:dm_detail', dmc_obj.dm.pk)


		elif aviso_obj.content_type.model == "directmessage":

			pk = aviso_obj.object_id
			dm_obj = DirectMessage.objects.get(id=pk)
			return redirect("direct_messages:dm_detail", dm_obj.pk)


		elif aviso_obj.content_type.model == "solicitud":

			solicitud_obj_pk = aviso_obj.object_id
			item_obj = Item.objects.get(solicitudes__id=solicitud_obj_pk)
			return redirect('solicitudes:solicitud_list', item_obj.pk)

		elif aviso_obj.content_type.model == 'itemcontact':

			item_contact_obj_pk = aviso_obj.object_id
			item_obj = Item.objects.get(item_contacts__id=item_contact_obj_pk)

			return redirect('items:item_detail', item_obj.id)








