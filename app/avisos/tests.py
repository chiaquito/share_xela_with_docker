####################################################################
# このtests.pyはavisoに関するテストに加え、シグナルに関するテストを記述する  #
#                                                                  #
####################################################################


from django.test import TestCase, RequestFactory
from django.test import Client
from django.urls import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from avisos.models import Aviso
from categories.models import Category
from api.models import DeviceToken
from items.models    import Item
from item_contacts.models import ItemContact
from profiles.models import Profile
from item_contacts.forms import ItemContactModelForm
from config.constants import ViewName, TemplateName, ContextKey
from config.tests.utils import pickUp_category_obj_for_test, create_item_contact_for_test
from config.tests.utils import create_user_for_test, create_user_data
from config.tests.utils import create_item_for_test, create_item_data
from config.tests.utils import create_solicitud_for_test, create_solicitud_data
from config.tests.utils import create_direct_message_for_test


#################################################
#           1. avisoに関するテスト               ##
#################################################

class AvisosAllListViewTestCase(TestCase):
    """テスト目的

    """
    """テスト対象
    avisos/views.py AvisosAllListView#get
    """
    """テスト項目
    特定のユーザーに結びつくavisoオブジェクトの表示ですべて表示される
    特定のユーザーに結びつくavisoオブジェクトが0個の場合aviso-listがテンプレートに描画されない
    """
    def setUp(self):
        """テスト環境
        特定のユーザーを作成する
        特定のユーザーに対するavisoオブジェクトを5個作成する
        """
        self.category_obj = pickUp_category_obj_for_test()
        self.user_obj, self.profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="test1"))
        #user_objが記事を作成する
        item_obj = create_item_for_test(self.user_obj, create_item_data(self.category_obj))
        

    def test_特定のユーザーに結びつくavisoオブジェクトの表示ですべて表示される(self):
        
        comment_user_obj, comment_user_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="comment_user"))
        
        # 5個のコメントを付す
        item_contact_obj = create_item_contact_for_test(comment_user_obj)
        item_contact_obj = create_item_contact_for_test(comment_user_obj)
        item_contact_obj = create_item_contact_for_test(comment_user_obj)
        item_contact_obj = create_item_contact_for_test(comment_user_obj)
        item_contact_obj = create_item_contact_for_test(comment_user_obj)

        # 全Avisoオブジェクトを取得する
        aviso_objects = Aviso.objects.filter(aviso_user=self.profile_obj)
        #print(aviso_objects.count())
        self.assertEqual(aviso_objects.count(), 5)

        # 記事作成者(user_obj)がAviso一覧ページにアクセスする
        self.client = Client()
        login_status = self.client.login(username=self.user_obj.username, password='1234tweet')
        aviso_all_url = reverse(ViewName.AVISO_ALL)
        response = self.client.get(aviso_all_url)
        avisos_response = response.context[ ContextKey.AVISO_OBJECTS ]
        self.assertEqual(avisos_response.count(), 5)

        # 返されるテンプレートにaviso-listタグが含まれていることを確認する
        self.assertContains( response, 'v-card', status_code=200 )


    
    def test_avisoオブジェクトが0のときはオブジェクトは0になる(self):
        # 記事作成者(user_obj)がAviso一覧ページにアクセスする
        self.client = Client()
        login_status = self.client.login(username=self.user_obj.username, password='1234tweet')
        aviso_all_url = reverse(ViewName.AVISO_ALL)
        response = self.client.get(aviso_all_url)
        avisos_response = response.context[ ContextKey.AVISO_OBJECTS ]
        self.assertEqual(avisos_response.count(), 0)


        


class AvisosListViewTestCase(TestCase):
    """テスト目的

    """
    """テスト対象
    avisos/views.py AvisosListView#get
    """
    """テスト項目
    特定のユーザーに結びつくavisoオブジェクトの表示で未読のみ表示される
    """
    def setUp(self):
        """テスト環境
        特定のユーザーを作成する
        特定のユーザーに対するavisoオブジェクトを5個作成する
        """
        self.category_obj = pickUp_category_obj_for_test()
        self.user_obj, self.profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="test1"))
        #user_objが記事を作成する
        item_obj = create_item_for_test(self.user_obj, create_item_data(self.category_obj))
        

    def test_特定のユーザーに結びつくavisoオブジェクトの表示で未読のみ表示される(self):
        
        comment_user_obj, comment_user_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="comment_user"))
        
        # 5個のコメントを付す
        item_contact_obj = create_item_contact_for_test(comment_user_obj)
        aviso_obj1 = Aviso.objects.filter(aviso_user=self.profile_obj).last()
        aviso_obj1.checked = True
        aviso_obj1.save()
        item_contact_obj = create_item_contact_for_test(comment_user_obj)
        item_contact_obj = create_item_contact_for_test(comment_user_obj)
        item_contact_obj = create_item_contact_for_test(comment_user_obj)
        item_contact_obj = create_item_contact_for_test(comment_user_obj)

        # 全Avisoオブジェクトを取得する
        aviso_objects = Aviso.objects.filter(aviso_user=self.profile_obj)
        #print(aviso_objects.count())
        self.assertEqual(aviso_objects.count(), 5)

        # 記事作成者(user_obj)がAviso一覧ページにアクセスする
        self.client = Client()
        login_status = self.client.login(username=self.user_obj.username, password='1234tweet')
        aviso_list_url = reverse(ViewName.AVISO_LIST)
        response = self.client.get(aviso_list_url)
        avisos_response = response.context[ ContextKey.AVISO_OBJECTS ]
        self.assertEqual(avisos_response.count(), 4)








##################################################
#           2. シグナルに関するテスト               ##
##################################################

class ItemContactPostSaveTest(TestCase):
    """テスト目的
    #item_contact_post_save_receiverについてのテスト avisos/models.py
    """
    """テスト対象
    avisos/models.py item_contact_post_save_receiver
    item_contacts/views.py 

    """
    """テスト項目
    済 ItemContactオブジェクトが生成されたらItem.item_contacts(ManyToManyField)に当該オブジェクトが追加される。*1
    済 ItemContactオブジェクトが生成されたらAvisoオブジェクトが少なくと1つ以上生成される。 *2
    保留 item_m2m_changed_receiver内のitem_contact_objectsが時系列順にItemContactオブジェクトが並んでいる。 *3
    済 item_contact_objは時系列順に並べたitem_contact_objectsのうち最後のオブジェクトである。*4
    済 コメント前のitem_contact_objectsのカウントが0の場合、記事作成者以外のユーザーがコメントすると生成されるAvisoオブジェクトは一つのみである。*5
    済 コメント前のitem_contact_objectsのカウントが0の場合、記事作成者以外のユーザーがコメントすると生成されるAvisoオブジェクトのaviso_user値は記事作成者のProfileオブジェクトである。*6
    済 コメント前のitem_contact_objectsのカウントが0の場合、記事作成者のユーザーがコメントすると生成されるAvisoオブジェクトは0個である。*7
    済 item_contact_objectsのカウントが0以外で生成されるAvisoオブジェクト数は記事作成者がコメントを送信する場合には、記事作成者を除くItemContactオブジェクトの重複なしのユーザー数と一致する。*8
    済 item_contact_objectsのカウントが0以外で生成されるAvisoオブジェクト数は記事作成者以外がコメントを送信する場合には、当該ユーザーを除くItemContactオブジェクトの重複なしのユーザー数と一致する。*9
    済 item_contact_objectsのカウントが0以外の場合、生成されるAvisoオブジェクトのaviso_user値はコメント送信者以外のProfileオブジェクトである。*10
    済 ダイレクトメッセージを送信するとAvisoオブジェクトが生成される

    """
    def setUp(self):
        """テスト環境

        Itemオブジェクト生成用のCategoryオブジェクト作成...category_obj
        Itemオブジェクトを作成した役のユーザーを作成...post_user
        Itemオブジェクト詳細ページにアクセスするユーザーを作成...access_user
        Itemオブジェクトを生成...item_obj1
        ItemContactオブジェクトを作成するユーザを生成...contact_user1      

        """
        category_obj = Category.objects.create(number="Donar o vender")
        post_user    = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        access_user  = User.objects.create_user(username="access_user", email="test_access_user@gmail.com", password='12345')
        item_obj1    = Item.objects.create(user=post_user, id=1, title="テストアイテム１", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        contact_user1 = User.objects.create_user(username="contact_user1", email="test_contact_user1@gmail.com", password='12345')
        contact_user2 = User.objects.create_user(username="contact_user2", email="test_contact_user1@gmail.com", password='12345')
        contact_user3 = User.objects.create_user(username="contact_user3", email="test_contact_user1@gmail.com", password='12345')


    def test_should_add_to_itemcontact_object_to_itemcontacts(self):
        # ItemContactオブジェクトが生成されたらItem.item_contacts(ManyToManyField)に当該オブジェクトが追加される。*1
        # ItemContactオブジェクトが生成されたらAvisoオブジェクトが少なくと1つ以上生成される。 *2
        item_obj1 = Item.objects.get(id=1)
        before_adding_itemcontact_count = item_obj1.item_contacts.all().count()
        self.assertEqual(before_adding_itemcontact_count, 0)
        contact_user1 = User.objects.get(username="contact_user1") # *1
        self.client = Client()
        login_status = self.client.login(username="contact_user1", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "ばばば"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証

        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)
        self.assertEqual(response.status_code, 200)
        templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.ITEM_DETAIL in templates)
        after_adding_itemcontact_count = Item.objects.get(id=1).item_contacts.all().count()
        self.assertEqual(after_adding_itemcontact_count, 1) # *1, *2 *5



    def test_should_be_old_first_order_od_itemcontact_objects(self):
        # item_m2m_changed_receiver内のitem_contact_objectsが時系列順にItemContactオブジェクトが並んでいる。 *3
        # item_contact_objは時系列順に並べたitem_contact_objectsのうち最後のオブジェクトである。*4
        self.client = Client()
        login_status = self.client.login(username="contact_user1", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), {'item_obj_id':1,  'message': "ばばば"}, follow=True)

        self.client = Client()
        login_status = self.client.login(username="contact_user2", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), {'item_obj_id':1,  'message': "びびび"}, follow=True)

        self.client = Client()
        login_status = self.client.login(username="contact_user3", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), {'item_obj_id':1,  'message': "ぶぶぶ"}, follow=True)

        item_contact_objects = response.context["item_contact_objects"]
        self.assertEqual(item_contact_objects.count(), 3)


    def test_should_add_to_itemcontact_object_to_itemcontacts_count0(self):
        # item_contact_objectsのカウントが0の場合、記事作成者以外のユーザーがコメントすると生成されるAvisoオブジェクトは一つのみである。*5
        # item_contact_objectsのカウントが0の場合、記事作成者以外のユーザーがコメントすると生成されるAvisoオブジェクトのaviso_user値は記事作成者のProfileオブジェクトである。*6
        item_obj1 = Item.objects.get(id=1)
        before_adding_itemcontact_count = item_obj1.item_contacts.all().count()
        self.assertEqual(before_adding_itemcontact_count, 0)
        self.assertEqual(Aviso.objects.all().count(),0)

        #contact_user1 = User.objects.get(username="contact_user1") # *1
        self.client = Client()
        login_status = self.client.login(username="contact_user1", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "ばばば"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証

        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)
        self.assertEqual(response.status_code, 200)
        #templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.ITEM_DETAIL in [ele.name for ele in response.templates])
        after_adding_itemcontact_count = Item.objects.get(id=1).item_contacts.all().count()
        self.assertEqual(after_adding_itemcontact_count, before_adding_itemcontact_count+1) # *5
        item_obj1 = Item.objects.get(id=1)
        self.assertEqual(Aviso.objects.filter(content_type=ContentType.objects.get(model="itemcontact")).first().aviso_user.user, item_obj1.user) # *6


    def test_should_no_be_created_aviso_by_owner_user(self):
        #コメント前のitem_contact_objectsのカウントが0の場合、記事作成者のユーザーがコメントすると生成されるAvisoオブジェクトは0個である。*7
        item_obj1 = Item.objects.get(id=1)
        before_adding_itemcontact_count = item_obj1.item_contacts.all().count()
        self.assertEqual(before_adding_itemcontact_count, 0)
        before_aviso_count = Aviso.objects.all().count()
        self.assertEqual(before_aviso_count,0)  
        self.client = Client()
        login_status = self.client.login(username="post_user", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "ばばば"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証

        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(TemplateName.ITEM_DETAIL in [ele.name for ele in response.templates])
        after_adding_itemcontact_count = Item.objects.get(id=1).item_contacts.all().count()
        self.assertEqual(after_adding_itemcontact_count, before_adding_itemcontact_count+1) # コメントを記述したのでアイテムコメントは1つ増えている
        self.assertEqual(Aviso.objects.filter(content_type=ContentType.objects.get(model="itemcontact")).count(), before_aviso_count)   


    def test_should_equal_aviso_objects_itemcontact_objects_by_owner(self): 
        #item_contact_objectsのカウントが0以外で生成されるAvisoオブジェクト数は記事作成者がコメントを送信する場合には、記事作成者を除くItemContactオブジェクトの重複なしのユーザー数と一致する。*8
        #item_contact_objectsのカウントが0以外で生成されるAvisoオブジェクト数は記事作成者以外がコメントを送信する場合には、当該ユーザーを除くItemContactオブジェクトの重複なしのユーザー数と一致する。*9
        #item_contact_objectsのカウントが0以外の場合、生成されるAvisoオブジェクトのaviso_user値はコメント送信者以外のProfileオブジェクトである。*10
        
        contact_user1 = User.objects.get(username="contact_user1")
        contact_user2 = User.objects.get(username="contact_user2")
        contact_user3 = User.objects.get(username="contact_user3")
        post_user     = User.objects.get(username="post_user")
        self.client = Client()
        login_status = self.client.login(username="contact_user1", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "ばばば"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)

        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "ばばば2"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)
        self.client = Client()
        login_status = self.client.login(username="contact_user2", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "びびび"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)

        self.client = Client()
        login_status = self.client.login(username="contact_user3", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "ぶぶぶ"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)

        #記事作成者がコメント送信する前の値チェック
        item_obj1 = Item.objects.get(id=1)
        item_contacts_count = item_obj1.item_contacts.all().count()
        self.assertEqual(item_contacts_count, 4)
        profiles = set([itemcontact.post_user for itemcontact in item_obj1.item_contacts.all()])
        profiles.discard(post_user)
        profiles_count = len(profiles)
        self.assertEqual(profiles_count, 3)
        before_aviso_objects_count_of_itemcontact = Aviso.objects.filter(content_type=ContentType.objects.get(model="itemcontact")).count()

        self.client = Client()
        login_status = self.client.login(username="post_user", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "ぶぶぶjjj"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)
        self.assertEqual(Item.objects.get(id=1).item_contacts.all().count(), item_contacts_count+1) #*8

        self.assertEqual(Aviso.objects.filter(content_type=ContentType.objects.get(model="itemcontact")).count(), before_aviso_objects_count_of_itemcontact+profiles_count)
        for aviso_obj in Aviso.objects.filter(content_type=ContentType.objects.get(model="itemcontact"))[before_aviso_objects_count_of_itemcontact+1:]:
            self.assertFalse(aviso_obj.aviso_user.user == post_user) # *10



    def test_should_equal_aviso_objects_itemcontact_objects_by_contact_user(self): 
        #item_contact_objectsのカウントが0以外で生成されるAvisoオブジェクト数は記事作成者以外がコメントを送信する場合には、当該ユーザーを除くItemContactオブジェクトの重複なしのユーザー数と一致する。*9
        
        
        contact_user1 = User.objects.get(username="contact_user1")
        contact_user2 = User.objects.get(username="contact_user2")
        contact_user3 = User.objects.get(username="contact_user3")
        post_user     = User.objects.get(username="post_user")
        self.client = Client()
        login_status = self.client.login(username="contact_user1", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "ばばば"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)

        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "ばばば2"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)
        self.client = Client()
        login_status = self.client.login(username="contact_user2", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "びびび"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)

        self.client = Client()
        login_status = self.client.login(username="contact_user3", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "ぶぶぶ"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)

        #記事作成者以外がコメント送信する前の値チェック
        item_obj1 = Item.objects.get(id=1)
        item_contacts_count = item_obj1.item_contacts.all().count()
        self.assertEqual(item_contacts_count, 4)
        profiles = set([itemcontact.post_user for itemcontact in item_obj1.item_contacts.all()])
        profiles.discard(contact_user3)
        profiles_count = len(profiles)
        self.assertEqual(profiles_count, 3)
        before_aviso_objects_count_of_itemcontact = Aviso.objects.filter(content_type=ContentType.objects.get(model="itemcontact")).count()

        self.client = Client()
        login_status = self.client.login(username="contact_user3", password='12345')
        self.assertTrue(login_status) #ログイン状態でアクセス
        #送信データの適切性検証
        data = {'item_obj_id':1,  'message': "ぶぶぶjjj"}
        form = ItemContactModelForm(data)
        self.assertTrue(form.is_valid()) #データの検証
        response = self.client.post(reverse(ViewName.ITEM_CONTACT), data, follow=True)
        self.assertEqual(Item.objects.get(id=1).item_contacts.all().count(), item_contacts_count+1) #*9
        
        self.assertEqual(Aviso.objects.filter(content_type=ContentType.objects.get(model="itemcontact")).count(), before_aviso_objects_count_of_itemcontact+profiles_count)



    def test_ダイレクトメッセージを送信するとAvisoオブジェクトが生成される(self):
        aviso_objects_count = Aviso.objects.all().count()
        self.assertEqual(aviso_objects_count, 0)
        category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="poosr"))
        item_obj = create_item_for_test(post_user_obj, create_item_data(category_obj))
        
        contact_user1, profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="contact_user1"))
        solicitud_obj = create_solicitud_for_test(item_obj, contact_user1, create_solicitud_data(message=None))
        new_aviso_objects_count = Aviso.objects.all().count()
        self.assertEqual(new_aviso_objects_count, aviso_objects_count+1)
        dm_obj, item_obj = create_direct_message_for_test(solicitud_obj)
        new1_aviso_objects_count = Aviso.objects.all().count()
        self.assertEqual(new1_aviso_objects_count, new_aviso_objects_count+1)

        
        self.client = Client()
        login_status = self.client.login(username=contact_user1.username, password='1234tweet')
        self.assertTrue(login_status) #ログイン状態でアクセス
        #送信データの作成
        data = {'profile':profile_obj,  'content': "ダイレクトメッセージのコンテント"}
        # ダイレクトメッセージをcontact_user1が送信する
        response = self.client.post(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=(str(dm_obj.id),)), data, follow=True)
        self.assertEqual(response.status_code, 200)
        after_aviso_objects_count = Aviso.objects.all().count()
        # Avisoオブジェクトが生成されたかチェック
        self.assertEqual(after_aviso_objects_count, new1_aviso_objects_count+1)





class UserPostSaveTest(TestCase):
    #user_post_save_receiverについてのテスト avisos/models.py
    """テスト項目

    済 Userオブジェクトが生成された時にProfileオブジェクトが生成される
    済 Userオブジェクトが変更された時にはProfileオブジェクトは生成されない

    //Userオブジェクトが新規に生成された時の属性値のチェック
    済 profile_obj.adm0 = "Guatemala"
    済 profile_obj.adm1 = "Quetzaltenango"
    済 profile_obj.adm2 = "Quetzaltenango"

    済 Userオブジェクトが生成された時にDeviceTokenオブジェクトが生成される
    済 Userオブジェクトが変更された時にDeviceTokenオブジェクトは生成されない
    済 Userオブジェクトが生成された時にはDeviceTokenオブジェクトのuser属性値は作成されたUserオブジェクトである
    済 Userオブジェクトが生成された時にはDeviceTokenオブジェクトのdevice_token属性値はNoneである

    """

    SIGN_UP_URL = "/accounts/signup/"
    SIGN_UP_DATA = {"email":"", "password1":"", "password2": ""}

    def setUp(self):
        self.client = Client()



    def test_profile_obj_is_created_by_user_obj_created(self):
        #Userオブジェクトが生成された時にProfileオブジェクトが生成される
        #このメソッドで新たにuserオブジェクトが作られるのでカウントが１になれば良い
        EXPECT = 1

        self.SIGN_UP_DATA["email"] = "hfhsifhidrgr@gmail.com"
        self.SIGN_UP_DATA["password1"] = "1234tweet"
        self.SIGN_UP_DATA["password2"] = "1234tweet"
        data = self.SIGN_UP_DATA
        response = self.client.post(self.SIGN_UP_URL, data)
        user_obj = User.objects.get(email=self.SIGN_UP_DATA["email"])
        profile_objects_count = Profile.objects.filter(user=user_obj).count()
        self.assertEqual(profile_objects_count, EXPECT, "PROFILEオブジェクトのadm0がGuatemalaになってないといけない")


    def test_profile_obj_is_not_created_by_user_obj_changed(self):
        #Userオブジェクトが変更された時にはProfileオブジェクトは生成されない
        #Userオブジェクトが作れれたときにProfileオブジェクトが作られるが、Userオブジェクトの変更では作られない。
        #したがってUserオブジェクトの変更前後でProfileオブジェクトのカウントは変わらなければ良い
        self.SIGN_UP_DATA["email"] = "hfhsifhidrgr@gmail.com"
        self.SIGN_UP_DATA["password1"] = "1234tweet"
        self.SIGN_UP_DATA["password2"] = "1234tweet"
        data = self.SIGN_UP_DATA
        response = self.client.post(self.SIGN_UP_URL, data)
        user_obj = User.objects.get(email=self.SIGN_UP_DATA["email"])
        profile_objects_count_before = Profile.objects.filter(user=user_obj).count()
        user_obj.email="wwwfhdsfhsiuhsivvs@gmail.com"
        user_obj.save()
        profile_objects_count_after = Profile.objects.filter(user=user_obj).count()
        self.assertEqual(profile_objects_count_before, profile_objects_count_after )


    def test_adm0_is_Guatemala(self):
        #profile_obj.adm0 = "Guatemala"である
        EXPECT = "Guatemala"        

        self.SIGN_UP_DATA["email"] = "hfhsifhidrgr@gmail.com"
        self.SIGN_UP_DATA["password1"] = "1234tweet"
        self.SIGN_UP_DATA["password2"] = "1234tweet"
        data = self.SIGN_UP_DATA
        response = self.client.post(self.SIGN_UP_URL, data)  
        user_obj = User.objects.get(email=self.SIGN_UP_DATA["email"])
        profile_obj = Profile.objects.get(user=user_obj)
        self.assertEqual(profile_obj.adm0, EXPECT, "PROFILEオブジェクトのadm0がGuatemalaになってないといけない")


    def test_adm1_is_Quetzaltenango(self):
        #profile_obj.adm1 = "Quetzaltenango"である
        EXPECT = "Quetzaltenango"

        self.SIGN_UP_DATA["email"] = "hfhsifhidrgr@gmail.com"
        self.SIGN_UP_DATA["password1"] = "1234tweet"
        self.SIGN_UP_DATA["password2"] = "1234tweet"
        data = self.SIGN_UP_DATA
        response = self.client.post(self.SIGN_UP_URL, data)  
        user_obj = User.objects.get(email=self.SIGN_UP_DATA["email"])
        profile_obj = Profile.objects.get(user=user_obj)
        self.assertEqual(profile_obj.adm1, EXPECT, "PROFILEオブジェクトのadm2がQuetzaltenangoになってないといけない")


    def test_adm2_is_Quetzaltenango(self):
        #profile_obj.adm2 = "Quetzaltenango"である
        EXPECT = "Quetzaltenango"

        self.SIGN_UP_DATA["email"] = "hfhsifhidrgr@gmail.com"
        self.SIGN_UP_DATA["password1"] = "1234tweet"
        self.SIGN_UP_DATA["password2"] = "1234tweet"
        data = self.SIGN_UP_DATA
        response = self.client.post(self.SIGN_UP_URL, data)  
        user_obj = User.objects.get(email=self.SIGN_UP_DATA["email"])
        profile_obj = Profile.objects.get(user=user_obj)
        self.assertEqual(profile_obj.adm2, EXPECT, "PROFILEオブジェクトのadm2がQuetzaltenangoになってないといけない")

    def test_should_create_device_token_obj_by_user_obj_created(self):
        #Userオブジェクトが生成された時にDeviceTokenオブジェクトが生成される

        #Userオブジェクト作成前
        before_device_token_objects_count = DeviceToken.objects.all().count()

        #Userオブジェクトを作成する
        self.SIGN_UP_DATA["email"] = "hfhsifhidrgr@gmail.com"
        self.SIGN_UP_DATA["password1"] = "1234tweet"
        self.SIGN_UP_DATA["password2"] = "1234tweet"
        data = self.SIGN_UP_DATA
        response = self.client.post(self.SIGN_UP_URL, data)
        after_device_token_objects_count = DeviceToken.objects.all().count()
        self.assertEqual(after_device_token_objects_count, before_device_token_objects_count +1)



    def test_should_not_create_device_token_obj_by_user_obj_changed(self):
        #Userオブジェクトが変更された時にDeviceTokenオブジェクトは生成されない


        #Userオブジェクトを作成する
        self.SIGN_UP_DATA["email"] = "hfhsifhidrgr@gmail.com"
        self.SIGN_UP_DATA["password1"] = "1234tweet"
        self.SIGN_UP_DATA["password2"] = "1234tweet"
        data = self.SIGN_UP_DATA
        response = self.client.post(self.SIGN_UP_URL, data)

        #Userオブジェクト変更前
        before_device_token_objects_count = DeviceToken.objects.all().count()

        #Userオブジェクト変更
        user_obj = User.objects.get(email="hfhsifhidrgr@gmail.com")
        user_obj.email = "hfhsifh1234r53idrgr@gmail.com"
        user_obj.save()

        #Userオブジェクト変更後
        after_device_token_objects_count = DeviceToken.objects.all().count()
        self.assertEqual(after_device_token_objects_count, before_device_token_objects_count)



    def test_should_be_user_obj_of_device_token_obj_user_attribute(self):
        #Userオブジェクトが生成された時にはDeviceTokenオブジェクトのuser属性値は作成されたUserオブジェクトである

        #Userオブジェクトを作成する
        self.SIGN_UP_DATA["email"] = "hfhsifhidrgr@gmail.com"
        self.SIGN_UP_DATA["password1"] = "1234tweet"
        self.SIGN_UP_DATA["password2"] = "1234tweet"
        data = self.SIGN_UP_DATA
        response = self.client.post(self.SIGN_UP_URL, data)

        user_obj = User.objects.get(email="hfhsifhidrgr@gmail.com")
        device_token_obj = DeviceToken.objects.all().first()
        self.assertEqual(device_token_obj.user, user_obj)



    def test_should_be_None_of_device_token_obj_devicetoken_attribute(self):
        #Userオブジェクトが生成された時にはDeviceTokenオブジェクトのdevice_token属性値はNoneである

        #Userオブジェクトを作成する
        self.SIGN_UP_DATA["email"] = "hfhsifhidrgr@gmail.com"
        self.SIGN_UP_DATA["password1"] = "1234tweet"
        self.SIGN_UP_DATA["password2"] = "1234tweet"
        data = self.SIGN_UP_DATA
        response = self.client.post(self.SIGN_UP_URL, data)

        user_obj = User.objects.get(email="hfhsifhidrgr@gmail.com")
        device_token_obj = DeviceToken.objects.all().first()
        self.assertEqual(device_token_obj.device_token, None)





