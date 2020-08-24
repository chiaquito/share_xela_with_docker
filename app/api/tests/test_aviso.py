from django.test import TestCase
from django.test import Client
from django.urls import reverse, reverse_lazy
from rest_framework.test import APIClient
from config.constants import ViewName
from django.contrib.auth.models import User
from config.tests.utils import (
    create_user_for_test, create_user_data,
    pickUp_category_obj_for_test,
    create_item_for_test, create_item_data
)


class ItemContactListByContactObjPKAPIViewTest(TestCase):

    """テスト対象
    api/views.py ItemContactListByContactObjPKAPIView#get

    endpoint: api/item_contact/<int:pk>/item_contacts/
    name: -
    """
    """テスト項目
    (ItemContactに関わる)AvisoオブジェクトからItemContactオブジェクツを返している
    (ItemContactに関わる)AvisoオブジェクトからItemContactオブジェクツを返している時、Itemオブジェクトを返している
    """
    def setUp(self):
        category_obj = pickUp_category_obj_for_test()
        post_user, post_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))
        access_user, access_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="access_user"))
        self.item_obj = create_item_for_test(post_user, create_item_data(category_obj))

    def test_ItemContactに関わるAvisoオブジェクトからItemContactオブジェクツを返す(self):

        # ItemContactオブジェクトを生成する。
        self.client = Client()
        post_user = User.objects.get(username="post_user")
        login_status = self.client.login(
            username="access_user", password="1234tweet")
        self.assertTrue(login_status)  # ログイン状態でアクセス
        data1 = {
            "post_user": post_user,
            "message": "message1",
            'item_obj_id': self.item_obj.id
            }
        self.client.post(reverse(ViewName.ITEM_CONTACT), data1)
        data2 = {
            "post_user": post_user,
            "message": "message2",
            'item_obj_id': self.item_obj.id
            }
        self.client.post(reverse(ViewName.ITEM_CONTACT), data2)
        data3 = {
            "post_user": post_user,
            "message": "message3",
            'item_obj_id': self.item_obj.id
            }
        self.client.post(reverse(ViewName.ITEM_CONTACT), data3)

        self.client = Client()
        login_status = self.client.login(
            username="post_user", password="1234tweet")
        response = self.client.get(reverse_lazy("avisos:avisos_alllist"))
        aviso_objects = response.context["aviso_objects"]
        for aviso_obj in aviso_objects:
            object_id = aviso_obj.object_id
            self.client = APIClient()
            self.client.force_authenticate(user=post_user)
            response = self.client.get(
                reverse_lazy(ViewName.ItemContactListByContactObjPKAPIView, args=(str(object_id),)))
            self.assertTrue('ITEM_CONTACT_OBJECTS' in response.data.keys())

    def test_ItemContactに関わるAvisoオブジェクトからItemContactオブジェクツを返している時Itemオブジェクトを返している(self):

        self.client = Client()
        post_user = User.objects.get(username="post_user")
        login_status = self.client.login(
            username="access_user", password="1234tweet")
        self.assertTrue(login_status)  # ログイン状態でアクセス
        data1 = {
            "post_user": post_user, "message": "message1", 'item_obj_id': self.item_obj.id}
        self.client.post(reverse(ViewName.ITEM_CONTACT), data1)
        data2 = {
            "post_user": post_user, "message": "message2", 'item_obj_id': self.item_obj.id}
        self.client.post(reverse(ViewName.ITEM_CONTACT), data2)
        data3 = {
            "post_user": post_user, "message": "message3", 'item_obj_id': self.item_obj.id}
        self.client.post(reverse(ViewName.ITEM_CONTACT), data3)

        self.client = Client()
        login_status = self.client.login(
            username="post_user", password="1234tweet")
        self.assertTrue(login_status)  # ログイン状態でアクセス
        response = self.client.get(reverse_lazy("avisos:avisos_alllist"))
        aviso_objects = response.context["aviso_objects"]
        for aviso_obj in aviso_objects:
            object_id = aviso_obj.object_id
            self.client = APIClient()
            self.client.force_authenticate(user=post_user)
            response = self.client.get(
                reverse_lazy(ViewName.ItemContactListByContactObjPKAPIView, args=(str(object_id),)))
            self.assertTrue('ITEM_OBJECT' in response.data.keys())
