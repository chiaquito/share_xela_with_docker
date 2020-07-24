from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.models import User
from solicitudes.models import Solicitud
from profiles.models     import Profile
from solicitudes.forms import SolicitudModelForm
from items.models import Item
from direct_messages.models import DirectMessage
# Create your views here.

from config.constants import ViewName, TemplateName



class SolicitudInputView(View):

	def get(self, request, *args, **kwargs):
		"""
		アイテム詳細ページの申請ボタンを押すと、メッセージフォームを表示する
		
		endpont: "solicitudes/item/<int:pk>/"
		name: "solicitudes:solicitud_input"
		"""
		"""テスト項目
		
		未認証ユーザーによるアクセスの場合には、認証ページにリダイレクトされる
		記事作成者でかつ認証したユーザーのアクセスの場合には、homeにリダイレクトされる
		認証ユーザーかつ記事作成者以外のアクセスの場合には"solicitudes/input_form.html"テンプレートが表示される。
		認証ユーザーかつ記事作成者以外のアクセスの場合にはcontextにキー"item_obj"が存在する
		認証ユーザーかつ記事作成者以外のアクセスの場合にはendpointに含まれるintに従って該当するidの記事が表示される。
		認証ユーザーかつ記事作成者以外のアクセスの場合にはcontextにキー"form"が存在する
		認証ユーザーかつ記事作成者以外のアクセスの場合にはcontextの"form"は"message"の項目がある

		"""

		pk = self.kwargs["pk"]
		item_obj = Item.objects.get(id=pk)


		#アクセスユーザーを制限
		# 未認証ユーザーの場合 -> 認証ページにリダイレクト
		if request.user.is_anonymous == True :
			return redirect('account_login')

		# Profileオブジェクトがない場合 -> Profileオブジェクト作成viewにリダイレクト(基本的にコレが実行されることは考えられない)
		elif Profile.objects.filter(user=request.user).count() == 0:
			return redirect('profiles:profile_setting')

		# 記事作成者がendpointにアクセスした場合 -> HOMEにリダイレクト
		elif request.user.username == item_obj.user.username:
			return redirect(ViewName.HOME)


		#表示するデータをcontextに格納する
		context = {}
		context["item_obj"] = item_obj
		form = SolicitudModelForm()
		context["form"] = form
		
		return render(request, TemplateName.SOLICITUD_INPUT, context)



	def post(self, request, *args, **kwargs):
		"""
		メッセージフォームの内容を受信し、Solicitudオブジェクトを生成する		
		そしてアイテム詳細ページにリダイレクトさせる
		メッセージフレームワークを使って"申請しました"と表示させる
		endpont: "solicitudes/item/<int:pk>/"
		name: "solicitudes:solicitud_input"		
		"""

		"""テスト項目
		未認証ユーザーによるアクセスの場合には、認証ページにリダイレクトされる
		記事作成者でかつ認証したユーザーのアクセスの場合には、homeにリダイレクトされる

		formの内容が不適切であればSolicitudオブジェクトは生成されない
		formの内容が不適切であれば"solicitudes/input_form.html"テンプレートが表示される。
		formの内容が適切であればSolicitudオブジェクトが新たに1つ生成される
		formの内容が適切であればItem詳細ページが表示される。
		新たに生成されたSolicitudオブジェクトのapplicant値はアクセスユーザーのProfileオブジェクトである。
		新たに生成されたSolicitudオブジェクトはintに対応するid値をもつItemオブジェクトのsolicitudesに含まれる。
		
		"""
		pk = self.kwargs["pk"]
		item_obj = Item.objects.get(id=pk)

		#アクセスユーザーを制限
		# 未認証ユーザーの場合 -> 認証ページにリダイレクト
		if request.user.is_anonymous == True :
			return redirect('account_login')

		# 記事作成者がendpointにアクセスした場合 -> HOMEにリダイレクト
		elif request.user.username == item_obj.user.username:
			return redirect(ViewName.HOME)


		form = SolicitudModelForm(request.POST)
		if form.is_valid():
			solicitud_obj = form.save(commit=False)
			applicant = Profile.objects.get(user=request.user)
			solicitud_obj.applicant = applicant
			solicitud_obj.save()

			#このオブジェクトをItemオブジェクトのsolicitudesフィールドに追加する
			item_obj.solicitudes.add(solicitud_obj)

			#m2mでAvisoオブジェクトを生成する

			return redirect(ViewName.ITEM_DETAIL, item_obj.id)
			
		else:			
			context["form"] = form
			return render(request, "solicitudes/input_form.html", context)





class GetSolicitudListForAvisoView(View):
	'''
	avisoのsolicitudオブジェクトpkを受け取り、
	Solicutudオブジェクト一覧を表示するSolicitudListViewにリダイレクトする
	'''
	
	def get(self, request, *args, **kwargs):
		
		solicitud_obj_pk = self.kwargs["pk"]
		solicitud_obj = Solicitud.objects.get(id=solicitud_obj_pk)
		return redirect('solicitudes:solicitud_decision', solicitud_obj.item.pk)





class SolicitudListView(View):

	def get(self, request, *args, **kwargs):
		"""機能
		Itemオブジェクト毎のsolicitudオブジェクトを一覧表示し、
		取引する相手を表示させるView
		endpoint: "solicitudes/item/<int:pk>/solicitud_list/"
		name: "solicitudes:solicitud_list"
		"""
		"""テスト項目

		未認証ユーザーによるアクセスの場合には、認証ページにリダイレクトする
		リクエストユーザーが記事作成者ではない場合にはHomeにリダイレクトする

		Itemオブジェクトのsolicitudesに含まれるSolicitudオブジェクトのうち一つがaccepted==Trueの場合にはDM詳細ページにリダイレクトされる
		contextに"solicitudes_objects"が存在する
		Itemオブジェクトのsolicitudesに含まれるSolicitudオブジェクトがもれなく適切に表示されている。
		contextに"item_obj"が存在する

		"""			

		pk = self.kwargs["pk"]
		item_obj = Item.objects.get(id=pk)
		#アクセスユーザーの制限

		#未認証ユーザーによるアクセスの場合には、認証ページにリダイレクトされる
		if request.user.is_anonymous == True :
			return redirect('account_login')
		# リクエストユーザーが記事作成者ではない場合 -> Homeにリダイレクト
		elif request.user.username != item_obj.user.username:
			return redirect(ViewName.HOME)


		#solicitudes_objects = Solicitud.objects.filter(item=item_obj)
		solicitudes_objects = item_obj.solicitudes.all()
		#申請者のうちTrue（取引相手が決まっている）の場合にはDirectMessage詳細ページを表示する
		for obj in solicitudes_objects:
			if obj.accepted == True:
				dm_obj = item_obj.direct_message
				return redirect('direct_messages:dm_detail', dm_obj.id)


		#ページに表示するデータをcontextに格納する
		context = {}
		context["item_obj"] = item_obj
		context["solicitudes_objects"] = solicitudes_objects
		return render(request, 'solicitudes/solicitud_decision.html', context )




class SolicitudSelectView(View):

	def post(self, request, *args, **kwargs):
		"""機能
		アイテムから記事作成者の選択肢した申請者を取引相手に定める

		endpoint: "solicitudes/solicitud/<int:pk>/select/"
		name: "solicitudes:solicitud_decision"
		"""
		"""テスト項目
		urlのintに合致するid値をもつSolicitudオブジェクトのaccepted値がTrueに変更される
		DM詳細ページにリダイレクトされる。


		"""
		pk = self.kwargs["pk"]
		solicitud_obj = Solicitud.objects.get(id=pk)
		#item_objを取得したい このとり方であっているか？
		item_obj = Item.objects.filter(solicitudes__id=solicitud_obj.id).first()		


		#アクセスユーザーの制限
		#未認証ユーザーによるアクセスの場合には、認証ページにリダイレクトされる
		if request.user.is_anonymous == True :
			return redirect('account_login')
		# リクエストユーザーが記事作成者ではない場合 -> Homeにリダイレクト
		elif request.user.username != item_obj.user.username:
			return redirect(ViewName.HOME)

		solicitud_obj.accepted = True
		solicitud_obj.save()

		#post_save()のシグナルでDirectMessageオブジェクトを生成する

		messages.info(request, "取引相手を決定しました。メッセージで詳細を決めてください。")
		return redirect("solicitudes:solicitud_list", item_obj.id)









