from avisos.models import Aviso
from config.utils import paginate_queryset
from config.constants import ContextKey, ViewName
from django.shortcuts import render, redirect
from django.views.generic import View
from direct_messages.models import DirectMessageContent
from direct_messages.models import DirectMessage
from items.models import Item
from item_contacts.models import ItemContact
from profiles.models import Profile
from solicitudes.models import Solicitud






class AvisosAllListView(View):
	"""機能
	未読既読の状態に関わらずすべての通知を表示する
	"""

	def get(self, request, *args, **kwargs):
		"""
		endpoint: /avisos/all/
		name: "avisos:avisos_alllist"
		"""

		if request.user.is_anonymous == True:
			#return redirect('account_login')
			return redirect(ViewName.ACCOUNT_LOGIN)

		elif Profile.objects.filter(user=request.user).exists() == False:
			return redirect('profiles:profile_creating')

		else:

			context = {}
			aviso_objects = Aviso.objects.filter(aviso_user=Profile.objects.get(user=request.user)).order_by("-created_at")
			aviso_count = Aviso.objects.filter(aviso_user=Profile.objects.get(user=request.user)).filter(checked=False).count()
			page_obj = paginate_queryset(request, aviso_objects)
			context[ ContextKey.AVISO_OBJECTS ] = page_obj.object_list
			context["aviso_count"] = aviso_count
			context[ ContextKey.PAGE_OBJ ] = page_obj
			context["type"] = "ALL"
			return render(request, 'avisos/avisos_prototype.html',context)




class AvisosListView(View):
	"""機能
	未読通知のみを表示する
	endpoint: "avisos/aviso/"
	name: "avisos:avisos_list"
	"""

	def get(self, request, *args, **kwargs):

		if request.user.is_anonymous == True:
			#return redirect('account_login')
			return redirect(ViewName.ACCOUNT_LOGIN)

		elif Profile.objects.filter(user=request.user).exists() == False:
			return redirect('profiles:profile_creating')
		else:
			context = {}
			aviso_objects = Aviso.objects.filter(aviso_user=Profile.objects.get(user=request.user)).filter(checked=False).order_by("-created_at")
			page_obj = paginate_queryset(request, aviso_objects)
			context[ ContextKey.AVISO_OBJECTS ] = page_obj.object_list
			context["aviso_count"] = aviso_objects.count()
			context[ ContextKey.PAGE_OBJ ] = page_obj
			context["type"] = "FILTERED"
			return render(request, 'avisos/avisos_prototype.html',context)



class AvisoCheckingView(View):

	def get(self, request, *args, **kwargs):
		"""機能
		Aviso一覧ページからAvisoを選択すると関連する通知対象のオブジェクトページにリダイレクトする

		pkからavisoオブジェクトをgetで取り出す。
		取り出したオブジェクトのcheckedをTrueに変更する。
		objectに基づいて各avisoの詳細ページにリダイレクトをかける。
		"""
		pk = self.kwargs["pk"]
		aviso_obj = Aviso.objects.get(id=pk)
		aviso_obj.checked = True
		aviso_obj.save()

		#aviso_objがなんのモデルを擁しているかを判定し、リダイレクトをかける
		#print(aviso_obj.content_type.model)


		#ダイレクトメッセージページにリダイレクトする
		if aviso_obj.content_type.model == "directmessagecontent":

			pk = aviso_obj.object_id
			dmc_obj = DirectMessageContent.objects.get(id=pk)
			#return redirect('direct_messages:dm_detail', dmc_obj.dm.pk)
			return redirect(ViewName.DIRECT_MESSAGE_DETAIL, dm_obj.pk)

		#ダイレクトメッセージページにリダイレクトする
		elif aviso_obj.content_type.model == "directmessage":
			pk = aviso_obj.object_id
			dm_obj = DirectMessage.objects.get(id=pk)
			#return redirect("direct_messages:dm_detail", dm_obj.pk)
			return redirect(ViewName.DIRECT_MESSAGE_DETAIL, dm_obj.pk)

		#申請者を選ぶページにリダイレクトする
		elif aviso_obj.content_type.model == "solicitud":
			solicitud_obj_pk = aviso_obj.object_id
			item_obj = Item.objects.get(solicitudes__id=solicitud_obj_pk)
			#return redirect('solicitudes:solicitud_list', item_obj.pk)
			return redirect(ViewName.SOLICITUD_LIST, item_obj.pk)

		#詳細記事ページにリダイレクトする
		elif aviso_obj.content_type.model == 'itemcontact':
			item_contact_obj_pk = aviso_obj.object_id
			item_obj = Item.objects.get(item_contacts__id=item_contact_obj_pk)
			#return redirect('items:item_detail', item_obj.id)
			return redirect(ViewName.ITEM_DETAIL, item_obj.id)








