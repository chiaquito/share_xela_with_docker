# coding: utf-8
import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from api.utils import getUserByToken
from config.tests.utils import (create_user_for_android_test)


class ProfileAPIViewGETTest(TestCase):
    """テスト目的

    """
    """テスト対象
    api/Views/profile_views.py ProfileAPIView#get

    endpoint: /api/profiles/
    name: -

    """
    """テスト項目
    済 keyを使ってこのエンドポイントにアクセスするとProfileデータを受け取る
    済 test_Tokenオブジェクトに存在しないkeyを使った場合rauthentication_failedの値が返る
    """
    def setUp(self):
        """共通環境
        Userオブジェクトを作成

        """
        self.PROFILE_URL = "/api/profiles/"
        self.post_user_key = create_user_for_android_test("post_user")

    def test_keyを使ってこのエンドポイントにアクセスするとProfileデータを受け取る(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        response = client.get(self.PROFILE_URL)
        # print(response.data)
        self.assertEqual(response.data["user"]["username"], "post_user")

    def test_Tokenオブジェクトに存在しないkeyを使った場合rauthentication_failedの値が返る(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + "dummy_key")
        response = client.get(self.PROFILE_URL)
        # print(response.data)
        # print(response.data["detail"])
        # print(type(response.data["detail"]))
        # print(dir(response.data["detail"]))
        # expect = ErrorDetail(string='Invalid token.')
        # print(response.data["detail"].code)
        # print(response.data["detail"].title)
        # print(type(response.data["detail"].code))
        self.assertEqual(response.data["detail"].code, "authentication_failed")


class ProfileAPIViewPATCHTest(TestCase):

    """テスト目的

    """
    """テスト対象
    api/Views/profile_views.py ProfileAPIView#patch

    endpoint: /api/profiles/
    name: -
    """
    """テスト項目
    usernameのみの変更を行う場合usernameの変更実行できる

    """
    def setUp(self):
        """共通環境
        Userオブジェクトを作成

        """
        self.PROFILE_URL = "/api/profiles/"
        # category_obj  = pickUp_category_obj_for_test()
        self.post_user_key = create_user_for_android_test("post_user")

    def test_usernameのみの変更を行う場合usernameの変更実行できる(self):
        # 変更前
        token_obj = Token.objects.get(key=self.post_user_key)
        user_obj = getUserByToken(token_obj)
        self.assertEqual(user_obj.username, "post_user")

        # 変更を行う
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)

        profile_data = json.dumps(
            {"user": {"username": "changedUsername"}}, ensure_ascii=False)
        response = client.patch(
            self.PROFILE_URL, profile_data, content_type="application/json")
        print(response.data)
        after_user_obj = getUserByToken(self.post_user_key)
        self.assertEqual(after_user_obj.username, "changedUsername")
        self.assertNotEqual(after_user_obj.username, user_obj.username)
