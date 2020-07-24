# coding: utf-8

from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse_lazy


from categories.models import Category
from items.models import Item
from django.contrib.auth.models import User
from config.tests.utils import *
from api.constants import SerializerContextKey





class ItemListAPIContextTest(TestCase):
    """テスト目的
    serializerContextにSerializerContextKey.ITEM_OBJECTSキーが含まれているので確認する
    """
    """テスト対象
    api.views.py ItemListAPIView (api:item_list)

    """

    """テスト項目

    認証されていないユーザーに対するserializerContext[SerializerContextKey.ITEM_OBJECTS]は"NO_SHOW"である。
    認証されたユーザーかつお気に入りを既にしているユーザーに対するcontext["btn_choice"]の値は"RED_HEART"である
    認証されたユーザーかつお気に入りをしていないユーザーに対するcontext["btn_choice"]の値は"WHITE_HEART"である

    """




class ItemFavoriteAPIViewTest(TestCase):
    """テスト目的
    Favボタンを押すことでItem.favorite_usersにFavoriteオブジェクトを追加または削除される機能を担保する
    """
    """テスト対象
    api.views.py ItemFavoriteAPIView#patch 

    endpoint: 'api/item/<int:pk>/favorite/'

    """
    """テスト項目
    済 お気に入りを既にしている認証されたユーザーがFavボタンを押した時に当該ユーザーのFavoriteオブジェクトがItem.favorite_usersから削除される *1
    済 お気に入りをしていない認証されたユーザーがFavボタンを押した時に当該ユーザーのFavoriteオブジェクトが生成され、Itemオブジェクトにそのオブジェクトが追加される *2
    """
    url = '/api/item/{}/favorite/'
    def setUp(self):
        """テスト環境
        Itemオブジェクト生成用のCategoryオブジェクト作成...category_obj
        Itemオブジェクトに対しFavボタンを押している役のユーザーを作成...fav_user
        Itemオブジェクトを作成した役のユーザーを作成...post_user
        Itemオブジェクト詳細ページにアクセスするユーザーを作成...access_user
        Itemオブジェクトを生成...item_obj1
        fav_userがFavボタンを押してFavoriteオブジェクトが生成される...fav_obj & item_obj1.favorite_users.add()部分
        """

        category_obj = Category.objects.create(number="Donar o vender")
        fav_user = User.objects.create_user(username="fav_user", email="fav_test_user@gmail.com", password='12345')
        post_user = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        access_user = User.objects.create_user(username="access_user", email="test_access_user@gmail.com", password='12345')
        item_obj1 =  Item.objects.create(user=post_user, id=1, title="テストアイテム１", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        item_obj1.favorite_users.add(fav_user)
        Token.objects.create(key="jjfogjosgjsr", user=access_user)
        Token.objects.create(key="jjfogjmkmvklsvmlosgjsr", user=fav_user)


        
    def test_should_remove_FavoriteObj_from_ItemObj_for_authenticated_user_with_favorite(self):
        # お気に入りを既にしている認証されたユーザーがFavボタンを押した時に当該UserオブジェクトがItem.favorite_usersから削除される *1
        item_obj1 =  Item.objects.get(id=1)
        token = Token.objects.get(user__username="fav_user")
        url = self.url.format(str(item_obj1.id))
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.patch(url)
        self.assertEqual(200, response.status_code)
        fav_user = User.objects.get(username="fav_user")
        users = [fav_obj.user for fav_obj in item_obj1.favorite_users.all()]
        self.assertTrue(fav_user not in users)
       


    def test_should_add_FavoriteObj_from_ItemObj_for_authenticated_user_with_favorite(self):
        # お気に入りをしていない認証されたユーザーがFavボタンを押した時には当該UserオブジェクトがItemオブジェクトのfavorite_usersに追加される *2
        item_obj1 =  Item.objects.get(id=1)
        url = self.url.format(str(item_obj1.id))

        token = Token.objects.get(user__username='access_user')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        access_user = User.objects.get(username="access_user")
        response = self.client.patch(url)
        self.assertEqual(200, response.status_code)
        item_obj1 = Item.objects.get(id=1)
        users = [fav_obj.username for fav_obj in item_obj1.favorite_users.all()]
        self.assertTrue(access_user.username in users)





class ItemDetailSerializerAPIViewGETTest(TestCase):


    """テスト目的
    endpointに対応する記事データを返していることを担保する


    """
    """テスト対象
    endpoint: "api/items/<int:pk>/"
    name: "item_detail"
    """
    """テスト項目
    済 ItemオブジェクトがResponseとして返される
    済 endpoint内のintに対応するidの記事データが返される
    済 ItemContactオブジェクトがItemオブジェクトのプロパティとしてResponseで返される
    済 UserオブジェクトがItemオブジェクトのプロパティとしてResponseで返される
    済 SolicitudオブジェクトがItemオブジェクトのプロパティとしてResponseで返される

    ユーザーのアクセス状態によってBTN_CHOICEを変更する

    """

    def setUp(self):
        """想定する共通の環境
        記事作成者(post_user)が記事を作成する。
        """
        #Solicitudオブジェクト、DirectMessageオブジェクトがないItemオブジェクトを生成

        category_obj = pickUp_category_obj_for_test()
        self.post_user_key = create_user_for_android_test(userName="post_user")
        self.item_obj1 = create_item_for_android_test(key=self.post_user_key, data=create_item_data_for_android_test(category_obj))
        
        #Solicitudオブジェクト、DirectMessageオブジェクトがないItemオブジェクトを生成
        self.item_obj2 = create_item_for_android_test(key=self.post_user_key, data=create_item_data_for_android_test(category_obj))
        

        self.item_obj3 = create_item_for_android_test(key=self.post_user_key, data=create_item_data_for_android_test(category_obj))




    def test_ItemオブジェクトがResponseとして返される(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        ITEM_DETAIL_URL = reverse_lazy("api:item_detail", args=(self.item_obj1.id,))
        response = client.get(ITEM_DETAIL_URL)
        self.assertTrue("item_obj_serializer" in response.data)




    def test_endpoint内のintに対応するidの記事データが返される(self):
        #(補足)検証する記事数は3つである

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        ITEM_DETAIL_URL = reverse_lazy("api:item_detail", args=(self.item_obj1.id,))
        response = client.get(ITEM_DETAIL_URL)

        #itemオブジェクトのidとResponseのItemオブジェクトのidが一致する内容を記述する
        self.assertEqual(response.data["item_obj_serializer"]["id"], self.item_obj1.id)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        ITEM_DETAIL_URL = reverse_lazy("api:item_detail", args=(self.item_obj2.id,))
        response = client.get(ITEM_DETAIL_URL)
        
        #itemオブジェクトのidとResponseのItemオブジェクトのidが一致する内容を記述する
        self.assertEqual(response.data["item_obj_serializer"]["id"], self.item_obj2.id)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        ITEM_DETAIL_URL = reverse_lazy("api:item_detail", args=(self.item_obj3.id,))
        response = client.get(ITEM_DETAIL_URL)
        print(response.data)

        #itemオブジェクトのidとResponseのItemオブジェクトのidが一致する内容を記述する
        self.assertEqual(response.data["item_obj_serializer"]["id"], self.item_obj3.id)


    def test_ItemContactオブジェクトがItemオブジェクトのプロパティとしてResponseで返される(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        ITEM_DETAIL_URL = reverse_lazy("api:item_detail", args=(self.item_obj1.id,))
        response = client.get(ITEM_DETAIL_URL)
        self.assertTrue("item_contacts" in response.data["item_obj_serializer"])


    def test_UserオブジェクトがItemオブジェクトのプロパティとしてResponseで返される(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        ITEM_DETAIL_URL = reverse_lazy("api:item_detail", args=(self.item_obj1.id,))
        response = client.get(ITEM_DETAIL_URL)
        self.assertTrue("user" in response.data["item_obj_serializer"])


    def test_SolicitudオブジェクトがItemオブジェクトのプロパティとしてResponseで返される(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        ITEM_DETAIL_URL = reverse_lazy("api:item_detail", args=(self.item_obj1.id,))
        response = client.get(ITEM_DETAIL_URL)
        self.assertTrue("solicitudes" in response.data["item_obj_serializer"])




class ItemDetailSerializerAPIViewPATCHTest(TestCase):


    """テスト目的
    endpointに対応する記事データが変更されるのを担保する

    androidの送信データは現状では、画像を除くデータはすべて送信される。変更されたかされていないか関係なく送信される。
    そしてデータのうち変更部分が変更反映される仕組みである。patchなので画像が送信されない限り、画像が削除されたりする変更されることがない。

    """
    """テスト対象
    endpoint: "api/items/<int:pk>/"
    name: "item_detail"
    """
    """テスト項目
    済 タイトルのみの変更の場合にはタイトルが変更される
    済 descriptionのみの変更の場合はdescriptionが変更される
    済 カテゴリーだけの変更の場合にはカテゴリーの変更が反映される
    済 radiusのみの変更の場合にはradiusが変更される
    pointのみの変更の場合にはpointが変更される
    adm1の変更の場合にはadm1が変更される
    adm2の変更の場合にはadm2が変更される


    """
    def setUp(self):
        """共通環境
        記事を作成する。
        """
        category_obj = pickUp_category_obj_for_test()
        self.post_user_key = create_user_for_android_test(userName="post_user")
        self.item_obj1 = create_item_for_android_test(key=self.post_user_key, data=create_item_data_for_android_test(category_obj))


    def test_タイトルのみの変更の場合にはタイトルが変更される(self):

        ITEM_DETAIL_URL = reverse_lazy("api:item_detail", args=(self.item_obj1.id,))

        #変更前
        item_obj1_before = Item.objects.get(title=self.item_obj1.title)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        response = client.get(ITEM_DETAIL_URL)
        self.assertEqual(response.data["item_obj_serializer"]["title"], item_obj1_before.title)        

        #変更及び変更データ
        data = create_item_data_for_android_test(category_obj=self.item_obj1.category, title="changed")

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        response = client.patch(ITEM_DETAIL_URL, data)
        self.assertEqual(response.data["result"], "success")
        item_obj1_after = Item.objects.get(description=self.item_obj1.description)
        self.assertEqual(item_obj1_after.title, "changed")
        self.assertNotEqual(item_obj1_before.title, item_obj1_after.title)


    def test_descriptionのみの変更の場合はdescriptionが変更される(self):

        ITEM_DETAIL_URL = reverse_lazy("api:item_detail", args=(self.item_obj1.id,))

        #print("確認")
        #print(self.item_obj1.title)

        #変更前
        item_obj1_before = Item.objects.get(title=self.item_obj1.title)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        response = client.get(ITEM_DETAIL_URL)
        self.assertEqual(response.data["item_obj_serializer"]["description"], item_obj1_before.description)        

        #変更及び変更データ *titleは入力しないと変わってしまう仕様なので入力している。変更はされていない。
        data = create_item_data_for_android_test(category_obj=self.item_obj1.category, title=self.item_obj1.title,description="changed")

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        response = client.patch(ITEM_DETAIL_URL, data)
        self.assertEqual(response.data["result"], "success")
        item_obj1_after = Item.objects.get(title=self.item_obj1.title)
        self.assertEqual(item_obj1_after.description, "changed")
        self.assertNotEqual(item_obj1_before.description, item_obj1_after.description)


    def test_カテゴリーだけの変更の場合にはカテゴリーの変更が反映される(self):

        ITEM_DETAIL_URL = reverse_lazy("api:item_detail", args=(self.item_obj1.id,))


        #変更前
        item_obj1_before = Item.objects.get(title=self.item_obj1.title)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        response = client.get(ITEM_DETAIL_URL)
        self.assertEqual(response.data["item_obj_serializer"]["category"]["number"], item_obj1_before.category.number)        

        #変更及び変更データ *titleは入力しないと変わってしまう仕様なので入力している。変更はされていない。
        changedCategoryObj = Category.objects.all().first()
        expected = changedCategoryObj.number
        data = create_item_data_for_android_test(category_obj=changedCategoryObj, title=self.item_obj1.title)
        
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        response = client.patch(ITEM_DETAIL_URL, data)
        self.assertEqual(response.data["result"], "success")
        item_obj1_after = Item.objects.get(title=self.item_obj1.title)
        self.assertEqual(item_obj1_after.category.number, expected)
        self.assertNotEqual(item_obj1_before.category.number, item_obj1_after.category.number)
        


    def test_radiusのみの変更の場合にはradiusが変更される(self):

        ITEM_DETAIL_URL = reverse_lazy("api:item_detail", args=(self.item_obj1.id,))

        #print("確認")
        #print(self.item_obj1.title)

        #変更前
        item_obj1_before = Item.objects.get(title=self.item_obj1.title)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        response = client.get(ITEM_DETAIL_URL)
        self.assertEqual(response.data["item_obj_serializer"]["radius"], item_obj1_before.radius)        

        #変更及び変更データ *titleは入力しないと変わってしまう仕様なので入力している。変更はされていない。
        data = create_item_data_for_android_test(category_obj=self.item_obj1.category, title=self.item_obj1.title, radius=1000)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.post_user_key)
        response = client.patch(ITEM_DETAIL_URL, data)
        self.assertEqual(response.data["result"], "success")
        item_obj1_after = Item.objects.get(title=self.item_obj1.title)
        self.assertEqual(item_obj1_after.radius, 1000)
        self.assertNotEqual(item_obj1_before.radius, item_obj1_after.radius)







