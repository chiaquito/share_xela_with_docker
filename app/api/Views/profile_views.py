from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework import parsers


from profiles.models import Profile
from api.utils import getTokenFromHeader, getUserByToken
from api.serializers import ProfileSerializer


class ProfileAPIView(APIView):

    #authentication_classes = (TokenAuthentication,) デフォルトなので必要ない 参照config/settogs.py
    #permission_classes = (permissions.IsAuthenticated,) デフォルトなので必要ない 参照config/settogs.py


    def get(self, request, *args, **kwargs):
        """
        profile情報を表示する
        
        endpoint: /api/profiles/
        name: -
        """
        """テスト項目
        済 keyを使ってこのエンドポイントにアクセスするとProfileデータを受け取る
        済 test_Tokenオブジェクトに存在しないkeyを使った場合rauthentication_failedの値が返る
        """
        
        #print(self.request.META)
        #print(self.request.META['HTTP_AUTHORIZATION'])

        #HTTPリクエストヘッダーのトークン情報からユーザーを特定する
        #token = self.request.META['HTTP_AUTHORIZATION'].split(" ")[1]

        token = getTokenFromHeader(self)
        #print(token)
        #Userオブジェクトの取得
        #user_obj = Token.objects.get(key=token).user
        user_obj = getUserByToken(token)
        if user_obj == None:
            return Response({"result":"fail"})
        profile_obj = Profile.objects.get(user=user_obj)
        #print(profile_obj)
        print(Response(ProfileSerializer(profile_obj).data))

        return Response(ProfileSerializer(profile_obj).data)



    def put(self, request, *args, **kwargs):
        #profileオブジェクトを更新する
        #画像変更が困る

        token = getTokenFromHeader(self)
        user_obj = getUserByToken(token)
        profile_obj = Profile.objects.get(user=user_obj)
        serializer = ProfileSerializer(profile_obj, data=request.data, partial=False)
        return Response({"result":"success"})





    def patch(self, request, *args, **kwargs):
        """機能
        Profileオブジェクトを更新する
        endpoint: api/profiles/
        """
        """テスト項目
        usernameのみの変更を行う場合usernameの変更実行できる

        """
        print(request.data)
        print(type(request.data))

        serializerContext = {}

        token = getTokenFromHeader(self)
        user_obj = getUserByToken(token)
        profile_obj = Profile.objects.get(user=user_obj)

        #print(request.data)


        #画像データが含まれている時 ->　画像も含めてProfileオブジェクトを更新する



        #画像データの送信と文字列データは別々に送信されるのでmultipart通信はありえないことが前提
        if len(request.FILES.keys()) > 0:
            print("TRUEが🐸")
            profile_obj.image = request.FILES["imageProfile"]
            profile_obj.save()

            serializerForSend = ProfileSerializer(Profile.objects.get(user=user_obj))
            serializerContext["PROFILE_OBJ"] = serializerForSend.data
            serializerContext["result"] = "success"
            Response(serializerContext)



        serializer = ProfileSerializer(profile_obj, data=request.data, partial=True)




        if serializer.is_valid() == False:
            #入力内容が変わってないとエラーが出るようだ。
            print("serializer.is_valid() : ",serializer.is_valid())
            text = ""
            for ele in serializer.errors:
                print(ele)
                text += ele +" / "

            return  Response({"result":"fail", "detail": text})





        #画像データが含まれていない時 ->　Profileオブジェクトを更新する
        if serializer.is_valid():
            print("ここ通ってる is_valid")
            print(request.data)
            #print(serializer)
            #print("serializer.is_valid() : ",serializer.is_valid())

            serializer._validated_data["user_obj_id"] = user_obj.id
            #print(serializer._validated_data)
            if "point" in request.data.keys():
                #aviso.modelsのシグナルを実行するためにmodel.save()を実行する
                serializer.save()
                serializer.instance.save(update_fields=["point"])
            else:
                serializer.save()

            #print(serializer.data)
            serializerForSend = ProfileSerializer(Profile.objects.get(user=user_obj))
            serializerContext["PROFILE_OBJ"] = serializerForSend.data
            serializerContext["result"] = "success"
            return Response(serializerContext)








