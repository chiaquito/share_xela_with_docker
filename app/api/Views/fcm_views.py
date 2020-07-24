from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework import parsers
#import json

from django.contrib.auth.models import User
from api.models import DeviceToken
from api.utils import getTokenFromHeader
from api.utils import getUserByToken




class DeviceTokenDealAPIVeiw(APIView):

    def patch(self, request, *args, **kwargs):
        """
        Android端末のデバイストークンが更新されたら新たなデバイストークンを既存のDeviceTokenオブジェクトに反映させる。
        Android側でトークンが変更される場合は以下の状況であり、その際にはAndroid側でonNewTokenコールバックを実行し、このViewに連結させる。
        https://firebase.google.com/docs/cloud-messaging/android/client?hl=ja#sample-register
        
        endpoint: /api/fcm/user/device_token/
        name: -
        """

        """テスト項目
        リクエストヘッダーに"token"が含まれていない場合のリクエストに対してResponse:failが返る
        リクエストヘッダーに"token"が含まれいるが不適切な値の場合のリクエストに対してResponse:failが返る
        リクエストヘッダーに"token"が含まれ値が適切な場合にはリクエストに対してResponse:successが返る


        """

        token   = getTokenFromHeader(self)
        userObj = getUserByToken(token)

        if userObj == None:
            return Response({"result":"fail"})

        #print(request.data)
        #print(request.data.keys())
        deviceToken = request.data['deviceToken']
        deviceTokenObj = DeviceToken.objects.get(user=userObj)
        deviceTokenObj.device_token = deviceToken
        deviceTokenObj.save()
        return Response({"result":"success"})







