from django.test import TestCase
from items.models import Item
from config.tests.utils import *
from config.constants import ViewName, TemplateName, ContextKey




class MyItemListViewTest(TestCase):
    """テスト目的
    
    """
    """テスト対象
    mypages/views.py MyItemListView#GET
    endpoint: "mypages/mylist"
    name: "mypages:item_mylist"
    """
    """テスト項目
    記事を一つも作成していないときには何もないことを示すテンプレートを表示する
    記事が作成してあるときは記事を閲覧するテンプレートが表示される
    表示される記事はすべてアクセスしたユーザが作成した記事である
    表示される記事にはactiveFalseが含まれない
    """

    def test_記事を一つも作成していないときには何もないことを示すテンプレートを表示する(self):
        item_count = Item.objects.all().count()
        self.assertEqual(item_count, 0)
        # 自分の記事を表示させる
        user_obj, profile_obj = create_user_for_test(create_user_data("test1"))
        self.client = Client()
        login_status = self.client.login(username="test1", password="1234tweet")
        self.assertTrue(login_status)
        response = self.client.get(reverse_lazy(ViewName.MY_LIST))
        # 返されるテンプレートの確認
        templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.NO_ITEMS in templates)


    def test_記事が作成してあるときは記事を閲覧するテンプレートが表示される(self):
        item_count = Item.objects.all().count()
        self.assertEqual(item_count, 0)
        # ユーザーが記事を作成する
        user_obj, profile_obj = create_user_for_test(create_user_data("test1"))
        category_obj = pickUp_category_obj_for_test()
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))

        self.client = Client()
        login_status = self.client.login(username="test1", password="1234tweet")
        self.assertTrue(login_status)
        response = self.client.get(reverse_lazy(ViewName.MY_LIST))
        # 返されるテンプレートの確認
        templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.ITEM_LIST in templates)


    def test_表示される記事はすべてアクセスしたユーザが作成した記事である(self):
        # ユーザーが記事を5コ作成する
        user_obj, profile_obj = create_user_for_test(create_user_data("test1"))
        category_obj = pickUp_category_obj_for_test()
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))
        # 関係ないユーザーが記事を３個作成する
        other_user_obj, other_profile_obj = create_user_for_test(create_user_data("other1"))
        item_obj = create_item_for_test(other_user_obj, create_item_data(category_obj))
        item_obj = create_item_for_test(other_user_obj, create_item_data(category_obj))
        item_obj = create_item_for_test(other_user_obj, create_item_data(category_obj))

        # 記事にアクセスする
        self.client = Client()
        login_status = self.client.login(username="test1", password="1234tweet")
        self.assertTrue(login_status)
        response = self.client.get(reverse_lazy(ViewName.MY_LIST))
        # 返されるコンテンツがすべてユーザーに関するものか確認
        item_objects = response.context[ ContextKey.ITEM_OBJECTS ]
        for item_obj in item_objects:
            self.assertEqual(item_obj.user, user_obj)
        # 返されるコンテンツの個数を確認
        self.assertEqual(item_objects.count(), 5)


    def test_表示される記事にはactiveFalseが含まれない(self):
        # ユーザーが記事を5コ作成する。そのうち2個はactiveをFalseに設定する
        user_obj, profile_obj = create_user_for_test(create_user_data("test1"))
        category_obj = pickUp_category_obj_for_test()
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))
        item_obj.active = False
        item_obj.save()
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))
        item_obj.active = False
        item_obj.save()
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))
        # 関係ないユーザーが記事を３個作成する
        other_user_obj, other_profile_obj = create_user_for_test(create_user_data("other1"))
        item_obj = create_item_for_test(other_user_obj, create_item_data(category_obj))
        item_obj = create_item_for_test(other_user_obj, create_item_data(category_obj))
        item_obj = create_item_for_test(other_user_obj, create_item_data(category_obj))

        # 記事にアクセスする
        self.client = Client()
        login_status = self.client.login(username="test1", password="1234tweet")
        self.assertTrue(login_status)
        response = self.client.get(reverse_lazy(ViewName.MY_LIST))
        # 返されるコンテンツがすべてユーザーに関するものか確認
        item_objects = response.context[ ContextKey.ITEM_OBJECTS ]
        for item_obj in item_objects:
            self.assertEqual(item_obj.user, user_obj)
        # 返されるコンテンツの個数を確認
        self.assertEqual(item_objects.count(), 3)        
