from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry


from avisos.models import Aviso
from categories.models import Category
from direct_messages.models import DirectMessage
from direct_messages.models import DirectMessageContent
from items.models import Item
from item_contacts.models import ItemContact
from item_contacts.forms import ItemContactModelForm


from prefecturas.models import Prefectura, Departamento, Municipio, RegionClassed


from profiles.models import Profile
from solicitudes.models import Solicitud

from .serializers import AvisoSerializer
from .serializers import CategorySerializer
from .serializers import ContactSerializer
from .serializers import DirectMessageContentSerializer
from .serializers import ItemContactSerializer
from .serializers import ItemSerializer
from .serializers import ProfileSerializer
from .serializers import UserSerializer
from .serializers import SolicitudSerializer

from .utils import getTokenFromHeader
from .utils import getUserByToken
from .constants import BtnChoice
from .constants import SerializerContextKey
from .constants import CategoryValue


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework import parsers

import json
import os




"""
*クラス命名規則*

基本的にRestfulな命名規則にしたい。

1インスタンスの参照、生成、修正、削除には、
"モデル名+APIView"として名付ける。

インスタンスのリストを参照する際は、
"モデル名+List+APIView"として名付ける。

いろいろな意味をもたせているクラスには、
"EX"を付加して名付ける。

状況を切り分けるためにリダイレクトを行うクラスには、
冒頭に"Sub"を付与する。

Serializerを使っているクラスには、
"SerializerAPIView"として名付ける。

"""

"""
得られた知見

基本的にGETのリクエストに対しては、データを返すことが見込まれるのでResponse({serializerContext})を返す。
POST,PATCHのリクエストに対しては、データを返すのではなく、結果を返すのでResponse({"result":"success"})のようなものを返すのが基本となる。

"""


class TestAPIView(APIView):

	authentication_classes = (BasicAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, *args, **kwargs):
		
		item_objects = Item.objects.all()
		serializer = ItemSerializer(item_objects, many=True)
		return Response(serializer.data)


class TestAPI2View(APIView):

	#authentication_classes = (TokenAuthentication,)
	#permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, *args, **kwargs):
		"""
		endpoint: items/test2/
		"""
		cat_obj = Category.objects.get(id=9)
		print(cat_obj.name)
		item_objects = Item.objects.all()
		item_obj = Item.objects.get(id=81)
		serializer = ItemSerializer(item_obj, many=False)
		return Response(serializer.data)



#AuthTokenが使えるか投げるためのView
class CheckAuthTokenView(APIView):
	"""
	endpoint: /api/checktoken/

	authTokenをSPから取って利用できるか確認する
	使える場合にはユーザーのProfileオブジェクトを返す。
	"""

	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, *args, **kwargs):
		serializerContext = {}
		
		token = getTokenFromHeader(self)
		user_obj = getUserByToken(token)
		if user_obj != None:
			token = Token.objects.get(user=user_obj)
			profile_obj = Profile.objects.get(user=user_obj)
			serializerContext["result"] = "success"
			serializer  = ProfileSerializer(profile_obj)
			serializerContext["PROFILE_OBJ"] = serializer.data
			serializerContext[SerializerContextKey.AUTH_TOKEN_KEY] = token.key

			return Response(serializerContext)

		return Response({"result":"fail"})
		
				




#最初に二股に分けるビューを経由させてから以下のビューに連結させる方がビューの役割をシンプルに保つことができるので、時間があったら修正する
#　というか以下はクラスじゃなくて関数でいい気がする。ただ関数を挟んでリダイレクトするとクエリを増やし、返す結果が遅くなってしまう
# 仮の案
class SubsolicitudListOrDirectMessageListAPIView(APIView):
	def get(self, request, *args, **kwargs):

		pk = self.kwargs["pk"]
		item_obj = Item.objects.get(id=pk)
		solicitudes_objects = Solicitud.objects.filter(item=item_obj)
		#申請者のうちTrue（取引相手が決まっている）の場合にはDirectMessage詳細ページを表示する
		for obj in solicitudes_objects:
			if obj.accepted == True:
				#dm_obj = DirectMessage.objects.get(item=item_obj)
				#return redirect('direct_messages:dm_detail', dm_obj.pk) #DirectMessageListAPIViewの呼び出し
				return redirect('api:DirectMessageContentListAPIView', item_obj.pk)

		return redirect('api:SolicitudListAPIView', item_obj.pk)  #SolicitudListAPIViewの呼び出し





# solicitudes/views.py SolicitudListViewに対応
# このビューは出品者がユーザーである場合に使われる
class SolicitudListAPIView(APIView):
	"""
	１アイテムごとのsolicitudオブジェクトを一覧表示し、
	取引する相手を決定するView
	endpoint "api/solicitud_list/<int:pk>/"
	"""
	def get(self, request, *args, **kwargs):

		serializerContext = {}

		pk = self.kwargs["pk"]
		#print("PKテスト",pk)
		item_obj = Item.objects.get(id=pk)
		solicitudes_objects = Solicitud.objects.filter(item=item_obj)
		#申請者のうちTrue（取引相手が決まっている）の場合にはDirectMessage詳細ページを表示する
		for obj in solicitudes_objects:
			if obj.accepted == True:
				dm_obj = DirectMessage.objects.get(item=item_obj)
				return redirect('direct_messages:dm_detail', dm_obj.pk)


		#context["item_obj"] = item_obj
		itemObjSerializer = ItemSerializer(item_obj1)
		serializerContext["ItemSerializerModel"] = itemObjSerializer.data

		#context["solicitudes_objects"] = solicitudes_objects
		solicitudesObjects = SolicitudSerializer(solicitudes_objects)
		serializerContext["SolicitudSerializer"] = solicitudesObjects.data

		return Response(serializerContext)

		#return render(request, 'solicitudes/solicitud_decision.html', context )



class SolicitudListAPIViewBySolicitudObjAPIView(APIView):
	"""
	android特有のAPI 決定するか一覧するかの表示を実施するもの
	endpoint: "api/solicitudes/solicitud/<int:pk>/solicitud_list/"
	name: -
	"""
	def get(self, request, *args, **kwargs):

		token = getTokenFromHeader(self)
		userObj = getUserByToken(token)

		if userObj == None:
			return Response({"result:fail"})

		solicitud_pk = self.kwargs["pk"]
		itemObj = Item.objects.get(solicitudes__id=solicitud_pk)

		if userObj != itemObj.user:
			return Response({"result:fail"})

		serializerContext = {}
		solicitudesObjects = itemObj.solicitudes.all()
		print(solicitudesObjects)
		solicitudesSerializer = SolicitudSerializer(solicitudesObjects, many=True)
		print(solicitudesSerializer.data)
		serializerContext["SOLICITUD_OBJECTS"] = solicitudesSerializer.data

		return Response(serializerContext)




class SolicitudAPIView(APIView):
	"""
	RestfulなAPIView

	"""

	def get(self, request, *args, **kwargs):
		"""
		endpoint: api/solicitud/<int:pk>

		getメソッドの結果を受け取るのはSolicitarDecideFragmentを想定している。
		SolicitarDecideFragment#newInstance()の引数はSolicitudオブジェクトである。
		このオブジェクトを解析して以下のデータを取得し画面に描画する。
		userName: User.username
		message: str
		profileImage: Profile.image

		"""

		#retrofitの送信でおそらくsolicitud_objectをBodyにせず、objIdをやってるのでそれを修正すること。

		serializerContext = {}
		#solicitudObjId = request.data["id"]
		solicitudObjId = self.kwargs["pk"]

		#print(solicitudObjId)

		solicitudObj   = Solicitud.objects.get(id=solicitudObjId)
		serializer = SolicitudSerializer(solicitudObj)
		serializerContext["SOLICITUD_OBJECT"] = serializer.data
		print(serializerContext)
		return Response(serializerContext)	



	# solicitudes/views.py SolicitudInputView#postに対応する
	#def post ユーザーが申請してインスタンスを生成する。
	def post(self, request, *args, **kwargs):
		"""
		endpoint: api/solicitudes/item/<int:pk>/
		"""

		item_obj_id = self.kwargs["pk"]
		item_obj    = Item.objects.get(id=item_obj_id)
		
		token = getTokenFromHeader(self)
		userObj = getUserByToken(token)
		profileObj = Profile.objects.get(user=userObj)

		message = request.data["message"]
		
		if SolicitudSerializer(data=request.data).is_valid():
			print("SERIALIZER.IS_VALID()  :  TRUE")
			solicitud_obj = Solicitud.objects.create(item=item_obj, applicant=profileObj , message=message )
			item_obj.solicitudes.add(solicitud_obj)

			return Response({"result": "success"})

		else:
			print("SERIALIZER.IS_VALID()  :  FALSE")
			for ele in serializer:
				print(ele)
			return Response({"result", "fail"})
		




	# solicitudes/views.py SolicitudListView#postに対応する
	def patch(self, request, *args, **kwargs):
		"""
		出品者が申請者を選んだ時に申請(solicitud)インスタンスのacceptedをTrueに修正する
		備考：
		Solicitudインスタンスをsave()すると、post_saveシグナルが発動し、DirectMessageオブジェクトが生成される。

		endpoint: api/solicitud/<int:pk>
		"""
		solicitud_obj_pk = self.kwargs["pk"]
		solicitud_obj = Solicitud.objects.get(id=solicitud_obj_pk)
		solicitud_obj.accepted = True
		solicitud_obj.save()


		itemObj = Item.objects.get(solicitudes__id=solicitud_obj_pk)
		serializer = ItemSerializer(itemObj)
		return Response({"result": "success",SerializerContextKey.ITEM_OBJ:serializer.data})









class ItemContactListAPIView(APIView):

	def get(self, request, *args, **kwargs):
		"""
		endpoint: api/item/<int:pk>/item_contacts/list/
		

		"""
		serializerContext = {}
		item_obj_id = self.kwargs["pk"]
		itemObj     = Item.objects.get(id=item_obj_id)
		itemSerializer = ItemSerializer(itemObj)
		serializerContext["ITEM_OBJECT"] = itemSerializer.data
		itemContactObjects = ItemContact.objects.filter(item=itemObj)
		itemContactSerializer  = ItemContactSerializer(itemContactObjects, many=True)
		serializerContext["ITEM_CONTACT_OBJECTS"] = itemContactSerializer.data

		return Response(serializerContext)




class ItemContactAPIView(APIView):

	def post(self, request, *args, **kwargs):
		"""
		ItemContactインスタンスを生成する
		endpoint: api/item_contacts/
		"""
		print("REQUEST.DATAのチェック")
		print(request.data)
		token = getTokenFromHeader(self)
		userObj = getUserByToken(token)
		profileObj = Profile.objects.get(user=userObj)
		item_obj_id = request.data["item"]["id"]
		item_obj = Item.objects.get(id=item_obj_id)
		message = request.data["message"]

		serializer = ItemContactSerializer(data=request.data)
		print(serializer.is_valid())
		if serializer.is_valid():
			#ItemContact.objects.create(post_user=profileObj, item=item_obj, message=message)
			itemContactObj = ItemContact.objects.create(post_user=profileObj, message=message)
			item_obj.item_contacts.add(itemContactObj)

		return Response({"result":"success"})





class ItemContactListByContactObjPKAPIView(APIView):

	def get(self, request, *args, **kwargs):
		"""
		ItemContactObjの一つから全体のItemContactのリストを取得する
		用途としてGeneric ForeignKeyのid(ItemContactのid)を受け取り、
		ItemContactオブジェクツのリスト表示を行うAvisoオブジェクトを選択した時に起動する

		endpoint: api/item_contact/<int:pk>/item_contacts/
		name: -

		改善点：単純にserializerContext["ITEM_CONTACT_OBJECTS"]が不要になった。Itemクラスに
		含まれるように変更したため。時間がある時に上記の項目とともにAndroidのロジックの修正を行う。
		(ホワイト)テストを書いていればその点も修正する。

		"""
		"""テスト項目　aviso系のtestファイルに記載

		(ItemContactに関わる)AvisoオブジェクトからItemContactオブジェクツを返している
		(ItemContactに関わる)AvisoオブジェクトからItemContactオブジェクツを返している時、Itemオブジェクトを返している

		"""

		serializerContext = {}
		itemContactId = self.kwargs["pk"]
		itemObj = Item.objects.get(item_contacts__id=itemContactId)
		itemSerializer = ItemSerializer(itemObj)
		serializerContext["ITEM_OBJECT"] = itemSerializer.data
		itemContactObjects = itemObj.item_contacts.all()
		itemContactSerializer = ItemContactSerializer(itemContactObjects, many=True)
		serializerContext["ITEM_CONTACT_OBJECTS"] = itemContactSerializer.data

		return Response(serializerContext)





class AreaSettingApiView(APIView):

	#authentication_classes = (TokenAuthentication,)
	#permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, *args, **kwargs):
		"""
		endpoint: "api/'area_setting/"

		"""
		from profiles.models import adm0_CHOICES, DEPARTAMENTO_CHOICES, MUNICIPIO_CHOICES

		adm0_list = [ele[0] for ele in adm0_CHOICES]
		adm1_list = [ele[0] for ele in DEPARTAMENTO_CHOICES]
		adm2_list = [ele[0] for ele in MUNICIPIO_CHOICES]

		serializer_context = {}

		#print("importがうまくできているか？？")
		#print(adm1_CHOICES)
		#print(adm1_list)
		serializer_context[SerializerContextKey.ADM0_LIST] = adm0_list
		serializer_context[SerializerContextKey.ADM1_LIST] = adm1_list
		serializer_context[SerializerContextKey.ADM2_LIST] = adm2_list

		return Response(serializer_context)




class AreaSettingWithGeoJsonApiView(APIView):

	#authentication_classes = (TokenAuthentication,)
	#permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, *args, **kwargs):
		"""
		endpoint: "api/'area_setting/"

		"""


		from profiles.models import adm0_CHOICES, DEPARTAMENTO_CHOICES, MUNICIPIO_CHOICES

		adm0_list = [ele[0] for ele in adm0_CHOICES]
		adm1_list = [ele[0] for ele in DEPARTAMENTO_CHOICES]
		adm2_list = [ele[0] for ele in MUNICIPIO_CHOICES]

		serializer_context = {}

		#print("importがうまくできているか？？")
		#print(adm1_CHOICES)
		#print(adm1_list)
		serializer_context[SerializerContextKey.ADM0_LIST] = adm0_list
		serializer_context[SerializerContextKey.ADM1_LIST] = adm1_list
		serializer_context[SerializerContextKey.ADM2_LIST] = adm2_list


		""" 便宜的にGeoJsonデータを追加する うまく行ったら別のViewを作成する"""
		token   = getTokenFromHeader(self)
		userObj = getUserByToken(token)
		print(token)
		print(userObj)
		profileObj = Profile.objects.get(user=userObj)
		depObjects = Departamento.objects.filter(adm1_es=profileObj.adm1)
		muniObjects = Municipio.objects.filter(adm2_es=profileObj.adm2)
		geoJson = serialize("geojson", depObjects)
		muniGeoJson = serialize("geojson", muniObjects)
		serializer_context["geoJsonData"] = geoJson
		serializer_context["muniGeoJson"] = muniGeoJson

		#print(serializer_context)

		return Response(serializer_context)





class GetRegionDataByPointAPIView(APIView):

	authentication_classes = ()
	permission_classes = ()

	def post(self, request, *args, **kwargs):
		"""機能
		wktのPOINTに基づいて対応するadm1, adm2を取得する

		endpoint: api/util/region/
		name: -
		もしかしてshpファイル自体が異なる可能性がある。これについては修正コストが高いのでこのままにしておく。
		-> dockerを使うとなぜかWKTを反転させないと使えないことが判明した。 
		"""
		"""テスト項目
		pointのwkt値がGuatemala内のQuezaltenangoの場合、adm1値はQuezaltenangoになる。
		pointのwkt値がGuatemala内のQuezaltenangoの場合、adm2値はQuezaltenangoになる。
		pointのwkt値がGuatemala国外のTapachulaの場合、adm1値はNoneになる。
		pointのwkt値がGuatemala国外のTapachulaの場合、adm2値はNoneになる。		
		"""
		adm1 = None
		adm2 = None

		wkt_point = request.data["wkt_point"]
		#test_wkt  = "SRID=4326;POINT(45.0000 45.000)"
		print("request.data[wkt_point]")
		print(wkt_point)

		launch_env = os.environ.get("LAUNCH_ENV", default="NO_DOCKER")
		if launch_env == "DOCKER":
			lng = wkt_point.split(" ")[1].replace("(", "")
			lat = wkt_point.split(" ")[2].replace(")", "")
			text = "POINT(" + lat + " " + lng + ")"
			point = GEOSGeometry(text)
		elif launch_env == "NO_DOCKER":
			point  = GEOSGeometry(wkt_point)



		#pointオブジェクト作成  WKTフォーマット: "SRID=4326;POINT(-91.5606545 14.8371541)"
		
		#point  = GEOSGeometry(wkt_point)

		dep_objects = Departamento.objects.all()
		for dep in dep_objects:
			#print(dep.geom.geom_type)
			central = dep.geom.centroid
			#print(central)
			#print(type(central))
			#print(dep.geom.contains(central))
			#print(point.within(dep.geom))

			if dep.geom.contains(point):
				adm1 = dep.adm1_es
				#print("発見")

		if adm1 == None:
			return Response({"adm1":adm1, "adm2": adm2}) #　値としてnullを返す

		rc_obj = RegionClassed.objects.get(departamento__adm1_es=adm1)
		for muni in rc_obj.municipios.all():
			if muni.geom.contains(point):
				adm2 = muni.adm2_es

		return Response({"adm1":adm1, "adm2":adm2})






class ContactAPIView(APIView):
	#endpoint: "api/contacts/"
	#スマホから入力された場合emailaddressにemailを送信機能を実装する余地がある

	#failを返す場合としてemailaddressが適切に入力されていない場合がある。

	authentication_classes = ()
	permission_classes = ()


	def post(self, request, *args, **kwargs):

		#ヘッダーにトークンが入っていればヘッダーからユーザーを特定する

		#データを取得するどうやって？


		print(request.data)
		serializer = ContactSerializer(data=request.data)
		#print(serializer.is_valid())
		#print(serializer.validated_data)
		if serializer.is_valid() == True:
			serializer.save()
			return Response({"result": "success"})

		elif serializer.is_valid() == False:
			return Response({"result": "fail"})

	





""" 						 DirectMessage 							"""


class DirectMessageContentListAPIView(APIView):
	"""
	却下案：DirectMessageオブジェクトのPKを受け取り、DirectMessageContentのリストを表示する
	ItemオブジェクトのPKを受け取り、DirectMessageContentのリストを表示する
	"""

	def get(self, request, *args, **kwargs):
		"""
		endpoint: item/<int:pk>/direct_message_content_list/
		"""
	
		serializerContext = {}
		pk      = self.kwargs["pk"]
		itemObj = Item.objects.get(id=pk)
		directMessageObj = DirectMessage.objects.get(item=itemObj)
		#dm_content_objects = DirectMessageContent.objects.filter(dm=directMessageObj)
		dm_content_objects = directMessageObj.direct_message_contents.all().order_by("created_at")
		DMCserializer = DirectMessageContentSerializer(dm_content_objects, many=True)
		serializerContext[SerializerContextKey.DM_CONTENT_OBJECTS_SERIALIZER] = DMCserializer.data

		token   = getTokenFromHeader(self)
		accessUserObj = getUserByToken(token)
		profileObj = Profile.objects.get(user=accessUserObj)
		profileSerializer = ProfileSerializer(profileObj)
		#もしかしてaccessUserObjのデータって必要ない??
		serializerContext["ACCESS_USER_PROFILE_SERIALIZER"] = profileSerializer.data
		return Response(serializerContext)




# direct_messages/api.py DirectMessageDetailView#post　に対応する
class DirectMessageContentAPIView(APIView):

	"""
	endpoint: direct_message_content/<int:pk>/

	Rest風なクラスビュー
	ただし、idをItemオブジェクトのidである

	pkはDirectMessageインスタンスとする

	"""
	def post(self, request, *args, **kwargs):
		"""
		endpoint: direct_message_content
		"""

		#print("REQUEST_DATAのチェック　：   ")
		#print(request.data)

		pk  = self.kwargs["pk"]

		itemObj = Item.objects.get(id=pk)
		dmObj = DirectMessage.objects.get(item=itemObj)
		token = getTokenFromHeader(self)
		userObj = getUserByToken(token)
		profileObj = Profile.objects.get(user=userObj)

		serializer = DirectMessageContentSerializer(data=request.data)
		if serializer.is_valid():
			print("SERIALIZER.IS_VALID : TRUE")

			dm_content_obj = DirectMessageContent.objects.create(profile=profileObj, content=request.data["content"] )
			dmObj.direct_message_contents.add(dm_content_obj)
			#dm_content_obj = serializer.save(commit=False)
			#dm_content_obj.dm = dmObj
			#dm_content_obj.profile = profileObj
			#dm_content_obj.save()
			return Response({"result":"success"})

		else:
			print("serializer.is_valid() : FALSE" )
			for ele in serializer:
				print(ele)
			return Response({"result": "fail"})







class ItemObjByDirectMessageContentObjPKAPIView(APIView):
	def get(self, request, *args, **kwargs):
		"""
		endpoint: direct_message_content/<int:pk>/ritem/

		DirectMessageContentオブジェクトIDを入力としてItemオブジェクトを返す。
		"""
		dm_contentObjId = self.kwargs["pk"]
		dm_contentObj   = DirectMessageContent.objects.get(id=dm_contentObjId)
		itemObj = dm_contentObj.dm.item
		serializer = ItemSerializer(itemObj)
		return Response(serializer.data)
		#return Response({"ITEM_OBJECT", serializer.data})





class AvisosAllListAPIView(APIView):

	def get(self, request, *args, **kwargs):


		"""コンテントタイプについて"""

		from django.contrib.contenttypes.models import ContentType
		#print("コンテントタイプ")
		#print(ContentType.objects.get(model='solicitud').id)
		#print(ContentType.objects.get(model='itemcontact').id)
		#print(ContentType.objects.get(model='directmessage').id)



		#userobjの取得
		token = getTokenFromHeader(self)
		userObj = getUserByToken(token)
		#print(userObj)

		#print(Profile.objects.filter(user=userObj).exists())

		if Profile.objects.filter(user=userObj).exists() == False: 

			#Profileオブジェクトを生成する必要がある
			return Response({"Profileについてどうするか考えておく":""})

		else:
			serializerContext = {}
			avisoObjects = Aviso.objects.filter(aviso_user=Profile.objects.get(user=userObj)).order_by("-created_at")

			serializer = AvisoSerializer(avisoObjects, many=True)
			#print(serializer.data)
			serializerContext["AVISO_OBJECTS"] = serializer.data
			return Response(serializerContext)











####################################
###     django-rest-authの継承    ###
####################################


from rest_auth.registration.views import RegisterView

class CustomeRegisterView(RegisterView):


	def create(self, request, *args, **kwargs):
		"""
		endpoint: api/custom/rest-auth/registration/
		name: 
		"""

		returned_obj = super().create(request, *args, **kwargs)

		#print(dir(returned_obj))
		#print(returned_obj.status_code)
		#print(returned_obj.data)
		#print(returned_obj.data())
		#print(returned_obj._headers)


		data = {}
		for key in returned_obj.data.keys():
			value = returned_obj.data[key]
			data[key] = value

		token = data["key"]
		user_obj = getUserByToken(token)
		data["username"] = user_obj.username

		return Response(data,
						returned_obj.status_code,
						returned_obj._headers)














import json
from django.http import HttpResponse
from prefecturas.models import Departamento
from prefecturas.functions import checkMultiPolygonMunicipio



class PrefecturaAPIView(APIView):

	def get(self, request, *args, **kwargs):
		"""
		geojsonで描画できるかをテストしただけのもの。
		現状は利用していない。
		endpoint : api/multipoly_test/
		"""


		print("-------------------------")		

		token = getTokenFromHeader(self)
		userObj = getUserByToken(token)
		#adm1_data = Profile.objects.get(user=userObj).adm1

		adm1_data = Profile.objects.get(user=User.objects.all().first()).adm1
		#print("ADM1_DATA")
		#print(adm1_data)


		#polyObjects = Prefectura.objects.filter(id=1)
		polyObjects = Departamento.objects.filter(adm1_es=adm1_data)
		#print(polyObjects)

		polyObj = Departamento.objects.get(adm1_es=adm1_data).geom
		#print(polyObj)



		test = serialize('geojson', polyObjects) #mpoly polygon geometry_field="",  fields=("geom")
		print(test)


		ts = json.loads(test)


		#print(type(ts)) #["geometry"]

		return Response({"test":ts})







