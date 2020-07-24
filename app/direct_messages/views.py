from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from profiles.models import Profile
from items.models import Item
from .models import DirectMessage
from .models import DirectMessageContent
from .forms import DirectMessageContentModelForm


from config.constants import ViewName





class DirectMessageDetailView(View):
	"""


	"""

	def get(self, request, *args, **kwargs):
		"""機能
		DMオブジェクトを参照するページを表示する
		閲覧できないのは、未認証ユーザーor DMオブジェクトに関連しないユーザー

	    endpoint: direct_messages/<int:pk>/
	    name: 'direct_messages:dm_detail'		
		"""
		#未認証ユーザーはDMオブジェクトを閲覧することはできない
		if request.user.is_anonymous:
			return redirect(ViewName.HOME)

		
		pk      = self.kwargs["pk"] 
		dm_obj  = DirectMessage.objects.get(id=pk)
		item_obj = Item.objects.get(direct_message__id=pk )

		dm_content_objects = dm_obj.direct_message_contents.all()
		#dm_content_objects = DirectMessageContent.objects.filter(dm=dm_obj)
		access_user_profile_obj = Profile.objects.get(user=User.objects.get(username=request.user.username))
		#user_obj = User.objects.get(username=request.user.username)

		# DMオブジェクトに関連しないユーザーはDMオブジェクトを閲覧することはできない
		if dm_obj.owner != access_user_profile_obj and dm_obj.participant != access_user_profile_obj:
			return redirect(ViewName.HOME)



		context = {}
		#data = { "dm":dm_obj, "profile":access_user_profile_obj }
		#form = DirectMessageContentModelForm(initial=data)
		form = DirectMessageContentModelForm()

		#form.fields["dm"].queryset = DirectMessage.objects.filter(id=pk)

		context["dm_obj"] = dm_obj
		context["dm_content_objects"] = dm_content_objects
		context["form"] = form
		context["item_obj"] = item_obj


		#context["BtnFeedback"]をセットするか否か
		#ユーザーがownerかparticipantか特定する。
		if dm_obj.owner == access_user_profile_obj and dm_obj.is_feedbacked_by_owner == False:
			context["btn_feedback"] = "btn_feedback"

		elif dm_obj.participant == access_user_profile_obj and dm_obj.is_feedbacked_by_participant == False:
			context["btn_feedback"] = "btn_feedback"

		return render(request, 'direct_messages/dm_detail.html', context)


	def post(self, request, *args, **kwargs):
		"""
		DirectMessageContentインスタンスを生成するメソッド。生成後は再度DirectMessageContentの一覧を表示させる
	    endpoint: direct_messages/<int:pk>/
	    name: 'direct_messages:dm_detail'
		"""
		pk      = self.kwargs["pk"]


		#アクセスユーザーの制限
		if request.user.is_anonymous:
			return redirect(ViewName.HOME)

		access_user_profile = Profile.objects.get(user=User.objects.get(username=request.user.username))
		dm_obj  = DirectMessage.objects.get(id=pk)
		if dm_obj.owner != access_user_profile and dm_obj.participant != access_user_profile:
			return redirect(ViewName.HOME)


		#context = {}
		
		form = DirectMessageContentModelForm(request.POST)
		#print(form)
		if form.is_valid():
			dm_content_obj = form.save(commit=False)
			dm_content_obj.profile = access_user_profile
			dm_content_obj.save()

			dm_obj.direct_message_contents.add(dm_content_obj)

			#messages.info(request, "メッセージを投稿しました。")
			messages.info(request, "Mensaje enviado")
			return redirect('direct_messages:dm_detail', pk)
		else:
			
			return redirect('direct_messages:dm_detail', pk)





class GetDirectMessageByUserListView(View):

	def get(self, request, *args, **kwargs):		
		#request.userをキーにDirectMessageオブジェクトを取り出し表示する
		context = {}

		post_user_dm_queryset = DirectMessage.objects.filter(post_user=request.user)
		solicitud_user_dm_queryset = DirectMessage.objects.filter(solicitud_user=request.user)
		dm_qs = DirectMessage.objects.none()
		dm_qs = dm_qs.union(post_user_dm_queryset, solicitud_user_dm_queryset)
		context["dm_qs"] = dm_qs
		context["type"] = "messages"
		#return render(request, "direct_messages/dm_list.html", context)
		return render(request, "avisos/avisos_list.html" ,context)
		



class GetDirectMessageByDirectMessageContentForAvisoView(View):
	"""
	DirectMessageContentオブジェクトのpkからダイレクトメッセージ画面を表示させる。
	"""
	def get(self, request, *args, **kwargs):
		pk = self.kwargs["pk"]
		dmc_obj = DirectMessageContent.objects.get(id=pk)

		return redirect('direct_messages:dm_detail', dmc_obj.dm.pk)




