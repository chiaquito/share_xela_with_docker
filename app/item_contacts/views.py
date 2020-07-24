from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

from config.constants import ViewName
from item_contacts.models import ItemContact
from item_contacts.forms import ItemContactModelForm

from items.models import Item
from items.models import Profile
from items.models import User







class ItemContactView(View):

	def post(self, request, *args, **kwargs):
		"""
		アイテムのコメント欄にコメントを追加するView

		endpoint: item_contacts/itemcontact/
		name: "item_contacts:ItemContactView"
		"""
		#print(request.POST)
		
		#ユーザー認証していない場合にはログインページへリダイレクトする。
		if request.user.is_anonymous == True:
			return redirect('account_login')


		#'item_obj_id' = request.POST.pop('item_obj_id', None)
		item_obj_id = request.POST['item_obj_id'] 
		item_obj = Item.objects.get(id=item_obj_id)
		post_user = Profile.objects.get(user=User.objects.get(username=request.user.username))
		form = ItemContactModelForm(request.POST)
		if form.is_valid():
			#print("ModelChoiceFieldは使えるのか？")
			item_contact_obj = form.save(commit=False)
			item_contact_obj.post_user = post_user
			
			item_contact_obj.save()
			item_obj.item_contacts.add(item_contact_obj)

			#m2mシグナルが起動する。 # avisos.models.py item_m2m_changed_receiverに連携

			#messages.info(request, "コメントを追加しました。")
			messages.info(request, "Comentario escrito")
			return redirect(ViewName.ITEM_DETAIL, item_obj_id)
		else:
			print("INVALID_DATA")
			return redirect(ViewName.ITEM_DETAIL, item_obj_id)






class ItemByItemContactView(View):

	"""
	ItemContactオブジェクトのpkからItemContactオブジェクトを取得し、
	それを利用してItem詳細ページを表示する

	このViewはAviso一覧ページにて使われている。


	バグがあるので後で処理する。
	"""

	def get(self, request, *args, **kwargs):
		pk = self.kwargs["pk"]
		item_contact_obj = ItemContact.objects.get(id=pk)
		item_obj = item_contact_obj.item  #バグ
		return redirect(ViewName.ITEM_DETAIL, item_obj.id)



