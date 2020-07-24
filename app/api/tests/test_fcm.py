from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from api.models import DeviceToken
from django.urls import reverse_lazy


class DeviceTokenDealAPIVeiwTest(TestCase):
    """テスト目的
    """
    """テスト対象
    api.Views.fcm_views.py DeviceTokenDealAPIVeiw#patch
        endpoint: /api/fcm/user/device_token/
        name: -
    """
    """テスト項目
    済 リクエストヘッダーに"token"が含まれていない場合のリクエストに対してResponse_failが返るリクエストヘッダーに"token"が含まれていない場合のリクエストに対してstatus_code_401が返る
    済 リクエストヘッダーに"token"が含まれているが不適切な値の場合のリクエストに対してResponse:failが返る
    済 リクエストヘッダーに"token"が含まれ値が適切な場合にはリクエストに対してResponse:successが返る
    済 適切な値のtokenがリクエストヘッダーに含まれている場合にはDeviceTokenオブジェクトのdevice_token値が更新される
    """

    def setUp(self):
        """テスト環境
        access_userを生成する
        access_userに対するtoken値を定める
        """
        access_user  = User.objects.create_user(username="access_user", email="test_access_user@gmail.com", password='12345')
        Token.objects.create(key="TOKEN_VALUE", user=access_user)
        dt_obj = DeviceToken.objects.get(user=access_user)
        dt_obj.device_token = "device_token_value"
        dt_obj.save()


    def test_リクエストヘッダーにtokenが含まれていない場合のリクエストに対してResponse_failが返る(self):

        #EXPECTED = 401
        EXPECTED = {"result":"fail"}

        self.client = APIClient()
        response = self.client.patch("/api/fcm/user/device_token/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, EXPECTED)


    def test_リクエストヘッダーにtokenが含まれているが不適切な値の場合のリクエストに対してstatus_code_401が返る(self):

        EXPECTED = 401

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +  'NO_TOKEN_VALUE')
        data = {"deviceToken": "CHANGE_DEVICE_TOKEN"}
        response = self.client.patch("/api/fcm/user/device_token/", data)
        self.assertEqual(response.status_code, EXPECTED)


    def test_リクエストヘッダーにtokenが含まれ値が適切な場合にはリクエストに対してResponse_successが返る(self):

        EXPECTED = {'result': 'success'}

        token = Token.objects.get(user__username="access_user")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +  token.key)
        data = {"deviceToken": "CHANGE_DEVICE_TOKEN"}
        response = self.client.patch("/api/fcm/user/device_token/", data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data, EXPECTED)

    
    def test_適切な値のtokenがリクエストヘッダーに含まれている場合にはDeviceTokenオブジェクトのdevice_token値が更新される(self):

        device_token_obj = DeviceToken.objects.get(user__username="access_user")
        self.assertEqual("device_token_value", device_token_obj.device_token)

        token = Token.objects.get(user__username="access_user")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +  token.key)
        data = {"deviceToken": "CHANGE_DEVICE_TOKEN"}
        response = self.client.patch("/api/fcm/user/device_token/", data)
        self.assertEqual(200, response.status_code)
        device_token_obj = DeviceToken.objects.get(user__username="access_user")
        self.assertEqual(device_token_obj.device_token, "CHANGE_DEVICE_TOKEN")               
    



