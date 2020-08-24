from django.test import TestCase
from items.models import Item
from item_contacts.models import ItemContact
from config.tests.utils import *
from config.constants import ViewName, TemplateName, ContextKey
from django.urls import reverse_lazy



class ItemContactViewPOSTTest(TestCase):
    """テスト目的
    
    """
    """テスト対象
    item_contacts/views.py ItemContactView#POST
    endpoint: "item_contacts/itemcontact"
    name: "item_cpntacts:itemcontact"
    """
    """テスト項目
    記事にコメントを追加するapiを叩くとコメントが追加される
    """

    def test_記事にコメントを追加するapiを叩くとコメントが追加される(self):
        item_count = Item.objects.all().count()
        self.assertEqual(item_count, 0)
        # 記事を作成する
        user_obj, profile_obj = create_user_for_test(create_user_data("test1"))
        category_obj = pickUp_category_obj_for_test()
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))
        # 別のユーザーを作成し、コメントを追加する
        comment_user, comment_profile = create_user_for_test(create_user_data("comment1"))
        self.client = Client()
        login_status = self.client.login(username="comment1", password="1234tweet")
        self.assertTrue(login_status)
        data = { "post_user": comment_user, "message":"メッセージ", "item_obj_id": item_obj.id }
        response = self.client.post(reverse_lazy(ViewName.ITEM_CONTACT), data)
        response = self.client.post(reverse_lazy(ViewName.ITEM_CONTACT), data)
        response = self.client.post(reverse_lazy(ViewName.ITEM_CONTACT), data)
        # コメントが３つ追加されているかチェックする 
        item_contacts = Item.objects.get(id=item_obj.id).item_contacts.all()
        self.assertEqual(item_contacts.count(), 3)

        # ページで表示する場合に描画されるコメント数をチェックする
        response = self.client.get(reverse_lazy(ViewName.ITEM_DETAIL, args=(str(item_obj.id),)))
        item_obj = response.context["item_obj"]
        self.assertEqual(item_obj.item_contacts.all().count(), 3)




'''
AvisoCheckingViewにて別のロジックに置き換えられたのでこのtestは不要となった。


class ItemByItemContactViewTest(TestCase):
    """テスト対象
    item_contacts/views.py ItemByItemContactView#GET
    endpoint: "item_contacts/itemcontact"
    name: "item_contacts:item_itemcontact"
    """
    """テスト項目
    記事についたコメントから記事が表示される
    """

    def test_記事についたコメントから記事が表示される(self):
        # 記事を作成する
        user_obj, profile_obj = create_user_for_test(create_user_data("test1"))
        category_obj = pickUp_category_obj_for_test()
        item_obj = create_item_for_test(user_obj, create_item_data(category_obj))
        # 別のユーザーを作成し、コメントを追加する
        comment_user, comment_profile = create_user_for_test(create_user_data("comment1"))
        self.client = Client()
        login_status = self.client.login(username="comment1", password="1234tweet")
        self.assertTrue(login_status)
        data = { "post_user": comment_user, "message":"メッセージ", "item_obj_id": item_obj.id }
        response = self.client.post(reverse_lazy(ViewName.ITEM_CONTACT), data)
        response = self.client.post(reverse_lazy(ViewName.ITEM_CONTACT), data)
        response = self.client.post(reverse_lazy(ViewName.ITEM_CONTACT), data)
        # コメントが３つ追加されているかチェックする 
        item_contacts = Item.objects.get(id=item_obj.id).item_contacts.all()
        self.assertEqual(item_contacts.count(), 3)

        # ページで表示する場合に描画されるコメント数をチェックする
        response = self.client.get(reverse_lazy(ViewName.ITEM_DETAIL, args=(str(item_obj.id),)))
        item_obj = response.context["item_obj"]
        self.assertEqual(item_obj.item_contacts.all().count(), 3)

        item_contact_obj = ItemContact.objects.all().first()
        self.client = Client()
        login_status = self.client.login(username="comment1", password="1234tweet")
        self.assertTrue(login_status)
        response = self.client.get(reverse_lazy("item_contacts:item_itemcontact", args=(str(item_contact_obj.id),)))
        res_item_obj = response.context["item_obj"]
        self.assertEqual(res_item_obj.id, item_obj.id)


        item_contact_obj = ItemContact.objects.all().last()
        self.client = Client()
        login_status = self.client.login(username="comment1", password="1234tweet")
        self.assertTrue(login_status)
        response = self.client.get(reverse_lazy("item_contacts:item_itemcontact", args=(str(item_contact_obj.id),)))
        res_item_obj = response.context["item_obj"]
        self.assertEqual(res_item_obj.id, item_obj.id)
'''