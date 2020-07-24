from django.test import TestCase, RequestFactory
from django.test import Client
from django.urls import reverse, reverse_lazy

from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

from config.constants import ViewName, TemplateName


from django.contrib.auth.models import User
from avisos.models import Aviso
from avisos.views import AvisosAllListView
from categories.models import Category
from items.models import Item
from item_contacts.models import ItemContact

from api.views import ItemContactListByContactObjPKAPIView




class ItemContactListByContactObjPKAPIViewTest(TestCase):

    """テスト目的
    
    """
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

        """テスト環境

        Itemオブジェクト生成用のCategoryオブジェクト作成...category_obj
        Itemオブジェクトを作成した役のユーザーを作成...post_user
        Itemオブジェクト詳細ページにアクセスするユーザーを作成...access_user
        Itemオブジェクトを生成...item_obj1
        ItemContactオブジェクトを作成するユーザを生成...contact_user1  
        Avisoオブジェクトを作成すること    

        """
        category_obj = Category.objects.create(number="Donar o vender")
        post_user    = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        access_user  = User.objects.create_user(username="access_user", email="test_access_user@gmail.com", password='12345')
        item_obj1    = Item.objects.create(user=post_user, id=1, title="テストアイテム１", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")



    def test_ItemContactに関わるAvisoオブジェクトからItemContactオブジェクツを返す(self):
        #ItemContactオブジェクトを生成する。
        self.client = Client()
        post_user = User.objects.get(username="post_user")
        login_status = self.client.login(username="access_user", password="12345")
        self.assertTrue(login_status) #ログイン状態でアクセス
        data1 = {"post_user":post_user, "message":"message1", 'item_obj_id':1 }
        self.client.post(reverse(ViewName.ITEM_CONTACT), data1)
        data2 = {"post_user":post_user, "message":"message2", 'item_obj_id':1}
        self.client.post(reverse(ViewName.ITEM_CONTACT), data2)
        data3 = {"post_user":post_user, "message":"message3", 'item_obj_id':1}
        self.client.post(reverse(ViewName.ITEM_CONTACT), data3)

        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")

        response = self.client.get(reverse_lazy("avisos:avisos_alllist"))
        aviso_objects = response.context["aviso_objects"]
        for aviso_obj in aviso_objects:
            object_id = aviso_obj.object_id
            self.client = APIClient()
            self.client.force_authenticate(user=post_user)
            response = self.client.get(reverse_lazy(ViewName.ItemContactListByContactObjPKAPIView, args=(str(object_id),)))
            self.assertTrue('ITEM_CONTACT_OBJECTS' in response.data.keys())




    def test_ItemContactに関わるAvisoオブジェクトからItemContactオブジェクツを返している時Itemオブジェクトを返している(self):

        self.client = Client()
        post_user = User.objects.get(username="post_user")
        login_status = self.client.login(username="access_user", password="12345")
        self.assertTrue(login_status) #ログイン状態でアクセス
        data1 = {"post_user":post_user, "message":"message1", 'item_obj_id':1 }
        self.client.post(reverse(ViewName.ITEM_CONTACT), data1)
        data2 = {"post_user":post_user, "message":"message2", 'item_obj_id':1}
        self.client.post(reverse(ViewName.ITEM_CONTACT), data2)
        data3 = {"post_user":post_user, "message":"message3", 'item_obj_id':1}
        self.client.post(reverse(ViewName.ITEM_CONTACT), data3)

        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")

        response = self.client.get(reverse_lazy("avisos:avisos_alllist"))
        aviso_objects = response.context["aviso_objects"]
        for aviso_obj in aviso_objects:
            object_id = aviso_obj.object_id
            self.client = APIClient()
            self.client.force_authenticate(user=post_user)
            response = self.client.get(reverse_lazy(ViewName.ItemContactListByContactObjPKAPIView, args=(str(object_id),)))
            self.assertTrue('ITEM_OBJECT' in response.data.keys())
















