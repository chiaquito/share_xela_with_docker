from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework import parsers
import json
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Q

from categories.models      import Category
from direct_messages.models import DirectMessage
from direct_messages.models import DirectMessageContent
from favorite.models        import Favorite
from items.models           import Item
from item_contacts.models   import ItemContact
from profiles.models        import Profile
from solicitudes.models     import Solicitud
 

from api.constants import SerializerContextKey
from api.constants import BtnChoice
from api.constants import CategoryValue

from api.serializers import ItemSerializer
from api.serializers import ProfileSerializer
from api.serializers import SolicitudSerializer
from api.serializers import ItemContactSerializer
from api.serializers import SolicitudSerializer



from api.utils import getTokenFromHeader
from api.utils import getUserByToken, getItemDetailUrl







class ItemListAPIView(APIView):
    """
    endpoint: 'items/list/'
    name: 'api:item_list'
    #dar,venderを一覧するView
    """

    def get(self, request, *args, **kwargs):
        serializerContext = {}
        item_objects = Item.objects.all().exclude(active=False).order_by("-created_at")
        serializer = ItemSerializer(item_objects, many=True)
        serializerContext[SerializerContextKey.ITEM_OBJECTS] = serializer.data

        return Response(serializerContext)





class ItemHomeListAPIView(APIView):
    """
    endpoint: 'api/items/home/list'
    name: "api:item_home_list"
    """
    def get(self, request, *args, **kwargs):
        serializerContext = {}
        #las cosas
        #item_objects_cosas = Item.objects.filter(category__number="1").filter(category__number="2").filter(category__number="3").order_by("-created_at")
        item_objects_cosas = Item.objects.filter(Q(category__number="1")|Q(category__number="2")|Q(category__number="3")).exclude(active=False).order_by("-id")
        serializer_cosas = ItemSerializer(item_objects_cosas, many=True)

        item_objects_habitacion = Item.objects.filter(Q(category__number="4")|Q(category__number="5")|Q(category__number="6")|Q(category__number="7")).exclude(active=False).order_by("-id")
        serializer_habitacion = ItemSerializer(item_objects_habitacion, many=True)

        item_objects_trabajo = Item.objects.filter(Q(category__number="8")|Q(category__number="9")).exclude(active=False).order_by("-id")
        serializer_trabajo = ItemSerializer(item_objects_trabajo, many=True)  

        item_objects_tienda = Item.objects.filter(category__number="10").exclude(active=False).order_by("-id")
        serializer_tienda = ItemSerializer(item_objects_tienda, many=True)               


        serializerContext[SerializerContextKey.ITEM_OBJECTS_COSAS]      = serializer_cosas.data
        serializerContext[SerializerContextKey.ITEM_OBJECTS_HABITACION] = serializer_habitacion.data
        serializerContext[SerializerContextKey.ITEM_OBJECTS_TRABAJO]    = serializer_trabajo.data
        serializerContext[SerializerContextKey.ITEM_OBJECTS_TIENDA]     = serializer_tienda.data
        return Response(serializerContext)








class ItemCategoryListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """機能

        endpoint: 'api/items/category/<int:pk>/items/list/'
        name: -
        """
        """テスト項目
        """
        category_number = self.kwargs["pk"]
        
        if category_number == 999:
            return redirect('api:item_home_list')
        elif category_number == 500:
            #500 --- Las Cosas...(1,2,3) dar o donar, busca donante, quiere avisarのカテゴリを一括にしたもの / categories.models.py 参照すること
            itemObjects = Item.objects.filter(Q(category__number="1")|Q(category__number="2")|Q(category__number="3")).exclude(active=False).order_by("-id")
            serializer  = ItemSerializer(itemObjects, many=True)
            serializerContext = {}
            serializerContext[SerializerContextKey.ITEM_OBJECTS] = serializer.data 
            return Response(serializerContext)

        elif category_number == 600:
            #600 --- Habitacion...(4,5,6,7) buscar habitacion, alquilar habitacion, dar pencionado, busco pencionista
            itemObjects = Item.objects.filter(Q(category__number="4")|Q(category__number="5")|Q(category__number="6")|Q(category__number="7")).exclude(active=False).order_by("-id")
            serializer = ItemSerializer(itemObjects, many=True)
            serializerContext = {}
            serializerContext[SerializerContextKey.ITEM_OBJECTS] = serializer.data 
            return Response(serializerContext)

        elif category_number == 700:
            #700 --- trabajo ...(8,9) buscar empleo, buscar trabajador
            itemObjects = Item.objects.filter(Q(category__number="8")|Q(category__number="9")).exclude(active=False).order_by("-id")
            serializer = ItemSerializer(itemObjects, many=True) 
            serializerContext = {}
            serializerContext[SerializerContextKey.ITEM_OBJECTS] = serializer.data 
            return Response(serializerContext)

        elif category_number == 800:
            #800 ___ Empresas y Servicios ...(10) publicidad de Enpresas y Servicios
            itemObjects = Item.objects.filter(category__number="10").exclude(active=False).order_by("-id")
            serializer = ItemSerializer(itemObjects, many=True) 
            serializerContext = {}
            serializerContext[SerializerContextKey.ITEM_OBJECTS] = serializer.data 
            return Response(serializerContext)

        

        #print(category_number)
        categoryObj = Category.objects.get(number=category_number)
        itemObjects = Item.objects.filter(category=categoryObj).exclude(active=False).exclude(active=False).order_by("-created_at")
        serializer  = ItemSerializer(itemObjects, many=True)
        serializerContext = {}
        serializerContext[SerializerContextKey.ITEM_OBJECTS] = serializer.data

        return Response(serializerContext)





class ItemCategoryLocalListAPIView(APIView):
    #dar,venderを一覧するView
    # このAPIViewを発行するときはクライアントは必ずユーザー認証が終わっているので、ユーザー認証等は考える必要ない。

    def get(self, request, *args, **kwargs):
        """機能

        endpoint: 'api/items/category/<int:pk>/items/list/local/'
        name: -
        """
        """テスト項目
        """
        
        token = getTokenFromHeader(self)
        userObj = getUserByToken(token)
        profileObj  = Profile.objects.get(user=userObj)

        category_number = self.kwargs["pk"]
        #print(category_number)
        categoryObj = Category.objects.get(number=category_number)
        itemObjects = Item.objects.filter(category=categoryObj).filter(adm1=profileObj.adm1).exclude(active=False).order_by("-created_at")
        serializer  = ItemSerializer(itemObjects, many=True)
        serializerContext = {}
        serializerContext[SerializerContextKey.ITEM_OBJECTS] = serializer.data 

        return Response(serializerContext)





class ItemFavoriteListAPIVIiew(APIView):
    """
    requestUserがのfav記事リスト一覧を表示する
    endpoint: 'items/user/item_favorite_list/'
    name: -s
    """

    def get(self, request, *args, **kwargs):

        #アクセスユーザーの制限
        token = getTokenFromHeader(self)
        requestUser = getUserByToken(token)
        if requestUser == None:
            return Response({"result": "fail"})

        favItemObjects = Item.objects.filter(favorite_users=requestUser).exclude(active=False)
        serializer = ItemSerializer(favItemObjects, many=True)


        #serializerContextに表示するデータを格納
        serializerContext={}
        serializerContext[SerializerContextKey.ITEM_OBJECTS] = serializer.data

        #成功した場合のレスポンスを返す
        return Response(serializerContext)







class ItemDetailSerializerAPIView(APIView):

    authentication_classes = ()
    #permission_classes = (permissions.IsAuthenticated,)    

    def get_object(self):

        try:
            pk = self.kwargs["pk"]
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Response({"result":"fail", "detail":"no exists"})




    def isChangedCategoryValue(self, item_obj, jsonData):
        """機能
        patchのみで使うメソッド
        patchで送信されたデータと変更対象となるデータの比較を行い、categoryだけ変更があった場合にはTrueを返す
        """
        
        if item_obj.category.number != jsonData["category"]["number"]:
            return True
        return False




    def get(self, request, *args, **kwargs):

        """機能
        endpointに対応する記事データを返す

        endpoint: "api/items/<int:pk>/"
        name: "item_detail"

        必要なオブジェクト
        item_obj, profile_obj, solicitudes_objects, direct_messages_objects
        ItemContactに関しては最新の５コメントしか表示しない仕様である。
        
        """
        """テスト項目
        済 ItemオブジェクトがResponseとして返される
        済 endpoint内のintに対応するidの記事データが返される
        済 ItemContactオブジェクトがItemオブジェクトのプロパティとしてResponseで返される
        済 UserオブジェクトがItemオブジェクトのプロパティとしてResponseで返される
        済 SolicitudオブジェクトがItemオブジェクトのプロパティとしてResponseで返される
        """

        
        pk = self.kwargs["pk"]
        item_obj = Item.objects.get(id=pk)
        item_obj_serializer = ItemSerializer(item_obj)
        user_obj = item_obj.user
        profile_obj = Profile.objects.get(user=item_obj.user)
        profile_obj_serializer  = ProfileSerializer(profile_obj)
        solicitudes_objects     = item_obj.solicitudes.all()
        solicitudSerializer     = SolicitudSerializer(solicitudes_objects, many=True)        
        item_contact_objects    = item_obj.item_contacts.all().order_by("-timestamp")[:5]
        item_contact_objects_serializer = ItemContactSerializer(item_contact_objects, many=True)
        direct_messages_objects = DirectMessage.objects.filter(item=item_obj)


        # 共通のデータをserializer_contextに格納する
        serializer_context = {}
        serializer_context["item_obj_serializer"] = item_obj_serializer.data
        serializer_context["profile_obj_serializer"] = profile_obj_serializer.data


        token = getTokenFromHeader(self)
        accessUser = getUserByToken(token)


        # serializer_context[SerializerContextKey.BTN_CHOICE]を設定
        if accessUser == None:
            serializer_context[SerializerContextKey.BTN_CHOICE] = BtnChoice.ANONYMOUS_USER_ACCESS

        elif accessUser == user_obj and solicitudes_objects.count() == 0:
            serializer_context[SerializerContextKey.BTN_CHOICE] = BtnChoice.NO_SOLICITUDES

        elif accessUser == user_obj and solicitudes_objects.count() != 0 and direct_messages_objects.count() == 0:
            serializer_context[SerializerContextKey.BTN_CHOICE] = BtnChoice.SELECT_SOLICITUDES

        elif accessUser == user_obj and direct_messages_objects.count() != 0:
            serializer_context[SerializerContextKey.BTN_CHOICE] = BtnChoice.GO_TRANSACTION

        elif accessUser != user_obj and solicitudes_objects.filter(applicant=Profile.objects.get(user=accessUser)).count() == 0 and direct_messages_objects.filter(item=item_obj).count() == 0:
            serializer_context[SerializerContextKey.BTN_CHOICE] = BtnChoice.SOLICITAR

        elif accessUser != user_obj and solicitudes_objects.filter(applicant=Profile.objects.get(user=accessUser)).count() != 0 and direct_messages_objects.count() == 0:
            serializer_context[SerializerContextKey.BTN_CHOICE] = BtnChoice.SOLICITADO

        elif accessUser != user_obj and direct_messages_objects.filter(participant=Profile.objects.get(user=accessUser)).count() == 1:
            serializer_context[SerializerContextKey.BTN_CHOICE] = BtnChoice.GO_TRANSACTION

        elif accessUser != user_obj and direct_messages_objects.filter(participant=Profile.objects.get(user=accessUser)).count() == 0:
            serializer_context[SerializerContextKey.BTN_CHOICE] = BtnChoice.CANNOT_TRANSACTION



        #データを送信
        return Response(serializer_context) 



    def patch(self, request, *args, **kwargs):
        """
        endpoint: /api/items/<int:pk>/
        name: -
        """
        """テスト項目
        タイトルのみの変更の場合にはタイトルが変更される。
        カテゴリーだけの変更の場合にはカテゴリーの変更が反映される。

        """
        pk = self.kwargs["pk"]
        item_obj = Item.objects.get(id=pk)

        print("ここ通っている？？？")
        print(request.data)

        strJsonData = request.data["jsonData"]
        jsonData = json.loads(strJsonData)

        #categoryName = jsonData.pop("category")["name"]
        #print("CATEGORY_NAME" + categoryName)
        #category_obj = Category.objects.get(name=categoryName)


        imagesData = request.FILES
        #print("IMAGES_DATA    :   ", imagesData)

        isChanged = self.isChangedCategoryValue(item_obj, jsonData)
        if isChanged == True:
            category_obj = Category.objects.get(number=jsonData["category"]["number"])
            item_obj.category = category_obj
            item_obj.save()


        serializer = ItemSerializer(item_obj, data=jsonData, partial=True)
        print("is_valid? : ",serializer.is_valid())
        if serializer.is_valid():
            serializer.save()

            itemId = serializer.instance.id
            url = getItemDetailUrl(itemId)

            if len(request.FILES.keys()) == 0:
                return Response({"result":"success", "detail":url })


            #if len(request.FILES.keys()) > 0:
            print("TRUEが🐸")
            #item_objに画像データを追加修正する。
            try:
                serializer.instance.image1 = imagesData[SerializerContextKey.IMAGE1]
                #item_obj.image1 = imagesData[SerializerContextKey.IMAGE1]
            except:
                pass
            try:
                serializer.instance.image2 = imagesData[SerializerContextKey.IMAGE2]
                #item_obj.image2 = imagesData[SerializerContextKey.IMAGE2]
            except:
                pass
            try:
                serializer.instance.image3 = imagesData[SerializerContextKey.IMAGE3]
                #item_obj.image3 = imagesData[SerializerContextKey.IMAGE3]
            except:
                pass

            serializer.instance.save()
            return Response({"result":"success", "detail":url })
            

        return Response({"result":"success", "detail":url })








#mypages/views.MyItemListViewに対応
class MyItemListSerializerAPIView(APIView):
    """
    endpoint: api/mylist/
    name: 
    """

    def get(self, request, *args, **kwargs):
        serializerContext = {}
        #ユーザー認証されていないときは、ログインページにつなぐ
        if request.auth == None:
            return Response({"result":"fail"})
            # Android端末では"ログインして下さい"を表示させる。

        #自分が作成した記事を表示する
        item_objects = Item.objects.filter(user=request.user).order_by("-created_at")
        if item_objects.count() > 0:
            
            item_objects_serializer = ItemSerializer(item_objects, many=True)

            print("maji??")
            #print(item_objects_serializer.data)
            return Response({"itemSerializer":item_objects_serializer.data})
        else:
            print("koko??")
            return Response({"itemSerializer":"jeje"})








class ItemFavoriteAPIView(APIView):

    def patch(self, request, *args, **kwargs):
        """
        endpoint: 'api/item/<int:pk>/favorite/'
        name: 'api:item_favorite'

        #機能：Item.favorite_users(ManyToManyField)にFavoriteオブジェクトを追加する。または削除する。
        機能：Item.favorite_users(ManyToManyField)にUserオブジェクトを追加する。または削除する。
        
        補足:
        このViewを通るのはすべて認証ユーザーである。
        未認証ユーザーがFavボタンを押しても、端末に”ログインしてください”と表示されるのみで通信が行われないから。
        
        """

        fav_status = None
        users   = []

        token       = getTokenFromHeader(self)
        requestUser = getUserByToken(token)
        itemObjId = self.kwargs["pk"]
        item_obj  = Item.objects.get(id=itemObjId)

        #item_obj.favorite_users.all()を使ってFavoriteオブジェクトに結びついたUserオブジェクトをリスト化する
        for user_obj in item_obj.favorite_users.all():
            users.append(user_obj)
            #if user_obj == requestUser:
            #    fav_status = "Favを既に押している"

        if requestUser in users:
            item_obj.favorite_users.remove(requestUser)

        elif requestUser not in users:
            item_obj.favorite_users.add(requestUser)

        return Response({"result":"success"})











class ItemCreateAPIViewMulti(APIView):

    """
    Itemオブジェクトを生成するために、
    user_obj, title, description, category_obj, adm0, adm1, adm2, image1, image2, image3を取得する。
    段階に分けて
    ① user_obj,
    ② category_obj,
    ③ title, description, adm0, adm1, adm2,
    ④ image1, image2, image3
    でItemオブジェクトを生成する。 

    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.MultiPartParser,)


    def post(self, request, *args, **kwargs):



        #① user_objを取得
        token = getTokenFromHeader(self)
        user_obj = getUserByToken(token)
        #print(token)

        #② category_objを取得
        #print("REQUEST_DATA")
        #print(request.data)
        strJsonData = request.data["jsonData"]
        jsonData = json.loads(strJsonData)
        #print(jsonData)

        categoryNumber = jsonData.pop("category")["number"]
        #print("CATEGORY_NAME" + categoryNumber)
        category_obj = Category.objects.get(number=categoryNumber)
        jsonData["category"] = category_obj.id

        #③ title, description, adm0, adm1, adm2を取得
        #serializer.is_valid()がTrueのとき各要素を取得する


        imagesData = request.FILES
        #print("IMAGES_DATA    :   ", imagesData)

        serializer = ItemSerializer(data=jsonData)

        if serializer.is_valid():
            print("SERIALIZER.IS_VALID : TRUE")
            
            item_obj = Item.objects.create(
                title = jsonData["title"],
                user = user_obj,
                description = jsonData["description"],
                price = jsonData["price"],
                category = category_obj,
                adm0 = jsonData["adm0"],
                adm1 = jsonData["adm1"], 
                adm2 = serializer.validated_data["adm2"]
                )

            try:
                point = jsonData["point"]
                item_obj.point = point
                item_obj.save()
            except:
                pass
            try:
                radius = jsonData["radius"]
                item_obj.radius = radius
                item_obj.save()
            except:
                pass

            
            url = getItemDetailUrl(item_obj.id)

            

            #print("ItemObject生成成功")

            if len(request.FILES.keys()) > 0:
                print("TRUEが🐸")
                #item_objに画像データを追加修正する。
                try:
                    item_obj.image1 = imagesData[SerializerContextKey.IMAGE1]
                except:
                    pass
                try:
                    item_obj.image2 = imagesData[SerializerContextKey.IMAGE2]
                except:
                    pass
                try:
                    item_obj.image3 = imagesData[SerializerContextKey.IMAGE3]
                except:
                    pass

                item_obj.save()
                return Response({"result":"success", "detail":url })

            return Response({"result":"success", "detail":url})   

        elif serializer.is_valid() == False:
            print("SERIALIZER.IS_VALID : False")
            for ele in serializer:
                print(ele)

            return  Response({"result":"fail"})













'''
# items/views.py ItemCreateView(View)に対応
class ItemCreateAPIView(APIView):

    """
    endpoint: 'api/item_create/'
    name: -

    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    #parser_classes = (parsers.MultiPartParser,)


    def post(self, request, *args, **kwargs):



        print("REQUEST.DATA   :   ")
        print(request.data)

        print(type(request.data))

        token = getTokenFromHeader(self)
        user_obj = getUserByToken(token)

        data = request.data
        categoryName = data.pop("category")["name"]
        category_obj = Category.objects.get(name=categoryName)

        

        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            print("SERIALIZER.IS_VALID : TRUE")
            #serializer.validated_data["user"] = user_obj
            
            item_obj = Item.objects.create(
                title = request.data["title"],
                user = user_obj,
                description = request.data["description"],
                category = category_obj,
                adm0 = request.data["adm0"],
                adm1 = request.data["adm1"], 
                #adm2 = request.data["adm2"]
                adm2 = serializer.validated_data["adm2"]
                )
            

            print("ItemObject生成成功")
            #item_obj.user = user_obj
            #item_obj.category = category_obj

            return Response({"result":"success"})

        elif serializer.is_valid() == False:
            print("SERIALIZER.IS_VALID : False")
            #print(serializer.error_messages)

            #print(serializer.user.error_messages)
            for ele in serializer:
                print(ele)


            #print(serializer.errors())

            return  Response({"result":"fail"})

'''

