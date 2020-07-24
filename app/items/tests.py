from django.test import TestCase, RequestFactory
from django.test.utils import setup_test_environment
from django.test import Client

from django.urls import reverse_lazy, reverse
from django.core.files import File
import mock

from django.contrib.auth.models import User
from items.forms import ItemModelForm
from items.models           import Item
from categories.models      import Category
from direct_messages.models import DirectMessage
from favorite.models        import Favorite
from profiles.models        import Profile
from solicitudes.models     import Solicitud


from config.constants import ViewName
from config.constants import TemplateName
from config.constants import ContextKey







'''
class ItemDetailBtnChoiceTest(TestCase):

    """テスト目的
    #item_detailでユーザー認証の状態によってbtn_choiceが適切に表示されることを担保したい

    """

    """テスト対象
    items.views.py ItemDetailView (items:item_detail)

    """

    """テスト項目

    認証されていないユーザーに対するcontext["btn_choice"]の値は"NO_SHOW"である。
    認証されたユーザーかつお気に入りを既にしているユーザーに対するcontext["btn_choice"]の値は"RED_HEART"である
    認証されたユーザーかつお気に入りをしていないユーザーに対するcontext["btn_choice"]の値は"WHITE_HEART"である

    """
'''


class ItemDetailContextDMObjTest(TestCase):

    """テスト目的
    #item_detailでDirectMessageオブジェクトがあればcontextにdm_objを追加する

    """

    """テスト対象
    items.views.py ItemDetailView (items:item_detail)

    """

    """テスト項目

    済 認証されていないユーザーの場合にはcontext["dm_obj"]のキーが存在しない。
    済 認証されたユーザーがユーザーが出品者の場合でかつそのユーザーを含むDirectMessageオブジェクトが存在する場合にはcontextに"dm_obj"のキーをもつ
    済 認証されたユーザーがユーザーが出品者でない場合かつそのユーザーを含むDirectMessageオブジェクトが存在する場合にはcontextに"dm_obj"のキーをもつ
    済 認証されたユーザーを含まないDirectMessageオブジェクトが存在する場合にはcontextに"dm_obj"のキーを持たない

    """

    ITEM_DETAIL_URL_FORMAT = "/items/item/{}/"
    DM_OBJ = "dm_obj"

    def setUp(self):
        category_obj = Category.objects.create(number="Donar o vender")
        post_user_obj = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        post_user_profile_obj = Profile.objects.get(user=post_user_obj)

        access_user_obj = User.objects.create_user(username="access_user", email="test_access_user@gmail.com", password='12345')
        #access_user_profile_obj = Profile.objects.get(user=access_user_obj)

        solicitud_user_obj = User.objects.create_user(username="solicitud_user", email="test_solicitud_user@gmail.com", password='12345')
        solicitud_user_profile_obj = Profile.objects.get(user=solicitud_user_obj)

        item_obj1 =  Item.objects.create(user=post_user_obj, id=1, title="テストアイテム１", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        dm_obj = DirectMessage.objects.create( owner=post_user_profile_obj, participant=solicitud_user_profile_obj)
        item_obj1.direct_message = dm_obj
        item_obj1.save()

    def test_should_be_NO_KEY_for_AnonymousUser日本語でもテストは通る(self):
        #認証されていないユーザーに対するcontextのキー["dm_obj"]はない。

        url = self.ITEM_DETAIL_URL_FORMAT.format("1")

        self.client = Client()
        client_login_status = self.client.logout()
        self.assertFalse(client_login_status) #未認証状態でアクセス

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200) #status_codeが200
        self.assertTrue(self.DM_OBJ not in response.context) #AnonymousUserの場合にはキーが存在しない
        

    def test_should_be_DM_OBJ_KEY_for_post_user(self):
        #認証されたユーザーがユーザーが出品者の場合でかつDirectMessageが存在する場合にはcontextに"dm_obj"のキーをもつ

        url = self.ITEM_DETAIL_URL_FORMAT.format("1")
        self.client = Client()
        client_login_status = self.client.login(username="post_user", password='12345')
        self.assertTrue(client_login_status) #認証状態でアクセス

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) #status_codeが200
        self.assertTrue(self.DM_OBJ in response.context) #キーが存在する。


    def test_should_be_DM_OBJ_KEY_for_access_user(self):
        #認証されたユーザーがユーザーが出品者でない場合かつDirectMessageが存在する場合にはcontextに"dm_obj"のキーをもつ

        url = self.ITEM_DETAIL_URL_FORMAT.format("1")
        self.client = Client()
        client_login_status = self.client.login(username="solicitud_user", password='12345')
        self.assertTrue(client_login_status) #認証状態でアクセス

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) #status_codeが200
        self.assertTrue(self.DM_OBJ in response.context) # キーが存在する。

    def test_should_be_NO_KEY_for_AuthenticatedUser(self):
        #認証されたユーザーを含まないDirectMessageオブジェクトが存在する場合にはcontextに"dm_obj"のキーを持たない

        url = self.ITEM_DETAIL_URL_FORMAT.format("1")
        self.client = Client()
        client_login_status = self.client.login(username="access_user", password='12345')
        self.assertTrue(client_login_status) #認証状態でアクセス

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) #status_codeが200
        self.assertTrue(self.DM_OBJ not in response.context) # 認証ユーザーでも、当該ユーザーがDirectMessageに含まれていなければキーは存在しない。





class ItemDetailContextBtnFavTest(TestCase):

    """テスト目的
    #item_detailでユーザー認証の状態によってbtn_favが適切に表示されることを担保したい

    """

    """テスト対象
    items.views.py ItemDetailView (items:item_detail)
    items.utils.py addBtnFavToContext

    """

    """テスト項目
    保留 item.favorite_usersに格納されるすべてのUserオブジェクトをusers: listに格納できている 
    保留 既にfavボタンを押しているユーザーのアクセスの場合fav_objはNoneではない。 
    保留 fav_obj.userはUserオブジェクトである
    済 未認証ユーザーの場合にはcontext["btn_fav"]の値が"NO_SHOW"である。 *4
    済 未認証ユーザーの場合にはcontext["fav_obj_id"]が存在しない。 *5
    済 アイテムにfavを押している認証ユーザーの場合にはcontext["btn_fav"]の値が"RED_HEART"である。 *3    
    済 アイテムにfavを押していない認証ユーザーの場合にはcontext["btn_fav"]の値が"WHITE_HEART"である。 *6

    """

    ITEM_DETAIL_URL_FORMAT = "/items/item/{}/"


    def setUp(self):
        """テスト環境

        Itemオブジェクト生成用のCategoryオブジェクト作成...category_obj
        Itemオブジェクトに対しFavボタンを押している役のユーザーを作成...fav_user
        Itemオブジェクトを作成した役のユーザーを作成...post_user
        Itemオブジェクト詳細ページにアクセスするユーザーを作成...access_user
        Itemオブジェクトを生成...item_obj1
        fav_userがFavボタンを押しitem_obj1.favorite_users.add()でfav_userが追加される。

        """

        category_obj = Category.objects.create(number="Donar o vender")
        fav_user = User.objects.create_user(username="fav_user", email="fav_test_user@gmail.com", password='12345')
        post_user = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        access_user = User.objects.create_user(username="access_user", email="test_access_user@gmail.com", password='12345')
        item_obj1 =  Item.objects.create(user=post_user, id=1, title="テストアイテム１", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        item_obj1.favorite_users.add(fav_user) 


    def test_should_be_NO_SHOW_for_anonymous_user(self):
        #未認証ユーザーの場合にはcontext["btn_fav"]の値が"NO_SHOW"である。 *4
       
        EXPECT = "NO_SHOW"        
        
        url = self.ITEM_DETAIL_URL_FORMAT.format("1")
        self.client = Client()
        login_status = self.client.logout()
        self.assertFalse(login_status) #未認証状態でアクセス
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        self.assertTrue("btn_fav" in response.context)
        self.assertEqual(response.context["btn_fav"], EXPECT, "context['btn_fav']=='NO_SHOW'でなければならない。")


    def test_should_be_without_fav_obj_id_for_anonymous_user(self):
        #未認証ユーザーの場合にはcontext["fav_obj_id"]が存在しない。 *5
        url = self.ITEM_DETAIL_URL_FORMAT.format("1")
        self.client = Client()
        login_status = self.client.logout()
        self.assertFalse(login_status) #未認証状態でアクセス
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        self.assertTrue("fav_obj_id" not in response.context)


    def test_should_be_RED_HEART_for_authenticated_user_with_fav(self):
        #認証されたユーザーかつ既にお気に入り済みユーザーに対するcontext["btn_fav"]の値は"RED_HEART"である *3

        EXPECT = "RED_HEART"
        url = self.ITEM_DETAIL_URL_FORMAT.format("1")
        self.client = Client()
        client_login = self.client.login(username="fav_user", password="12345")
        self.assertTrue(client_login) #認証状態でアクセス
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("btn_fav" in response.context)
        self.assertEqual(response.context["btn_fav"], EXPECT, "context['btn_fav']=='RED_HEART'でなければならない。")


    def test_should_be_WHITE_HEART_for_authenticated_user_without_fav(self):
        # アイテムにfavを押していない認証ユーザーの場合にはcontext["btn_fav"]の値が"WHITE_HEART"である。 *6
        EXPECT = "WHITE_HEART"

        url = self.ITEM_DETAIL_URL_FORMAT.format("1")
        self.client = Client()
        client_login = self.client.login(username="access_user", password="12345")
        self.assertTrue(client_login) #認証状態でアクセス
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("btn_fav" in response.context)
        self.assertEqual(response.context["btn_fav"], EXPECT)



class ItemListByFavorite(TestCase):
    """テスト目的
    認証されたユーザーのFavボタンが押されたItemのリストを表示する
    """
    """テスト対象
    items/views.py ItemListByFavoriteView
    endpoint: 'items/user/favorite/'
    name: 'items:item_list_by_favorite'    
    """
    """テスト項目
    未認証ユーザーによるアクセスの場合にはhomeにリダイレクトする *1
    認証されたユーザーのアクセスの場合はItem.favorite_usersに認証されたユーザーオブジェクトが含まれるものだけを表示する *2
    """

    def setUp(self):
        """テスト環境
        検証対象のユーザー(fav_user)がFavボタンを押したアイテムを以下のものとする。
        item_obj1
        item_obj2
        item_obj5
        """
        category_obj = Category.objects.create(number="Donar o vender")
        fav_user = User.objects.create_user(username="fav_user", email="fav_test_user@gmail.com", password='12345')
        post_user = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        access_user = User.objects.create_user(username="access_user", email="test_access_user@gmail.com", password='12345')
        item_obj1 = Item.objects.create(user=post_user, id=1, title="テスト1", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        item_obj1.favorite_users.add(fav_user)

        item_obj2 = Item.objects.create(user=post_user, id=2, title="テスト2", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        item_obj2.favorite_users.add(fav_user)

        item_obj3 = Item.objects.create(user=post_user, id=3, title="テスト3", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")

        item_obj4 = Item.objects.create(user=post_user, id=4, title="テスト4", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")

        item_obj5 = Item.objects.create(user=post_user, id=5, title="テスト5", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        item_obj5.favorite_users.add(fav_user)



    def test_should_be_list_of_1_2_5(self):
        # 未認証ユーザーによるアクセスの場合にはhomeにリダイレクトする *1
        # 認証されたユーザーのアクセスの場合はItem.favorite_usersに認証されたユーザーオブジェクトが含まれるものだけを表示する *2

        self.client = Client()
        login_status = self.client.logout()
        self.assertFalse(login_status) #未ログイン状態でアクセス 
        response = self.client.get(reverse('items:item_list_by_favorite'), follow=True)
        #response = self.client.get(reverse('items:item_list_by_favorite'), follow=True)
        #response = self.client.get(reverse(ViewName.ITEM_LIST_BY_FAVORITE), follow=True)
        templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.HOME in templates) #*1

        self.client = Client()
        login_status = self.client.login(username="fav_user", password="12345")
        self.assertTrue(login_status) #ログイン状態でアクセス

        response = self.client.get(reverse_lazy(ViewName.ITEM_LIST_BY_FAVORITE), follow=True)
        item_objects = response.context[ContextKey.ITEM_OBJECTS]
        self.assertTrue(item_objects.count(), 3)
        self.assertTrue(Item.objects.get(id=1) in item_objects)
        self.assertTrue(Item.objects.get(id=2) in item_objects)
        self.assertTrue(Item.objects.get(id=3) not in item_objects)         
        self.assertTrue(Item.objects.get(id=4) not in item_objects)
        self.assertTrue(Item.objects.get(id=5) in item_objects) #*2








class ItemFavoriteViewTest(TestCase):

    """テスト目的
    FavBtnを押したらItem.favorite_usersにUserオブジェクトが追加されるかまたは削除される動作の信頼性を担保する

    """

    """テスト対象
    items.views.py ItemFavoriteView (items:item_detail)
    endpoint: 'items/item/<int:pk>/favorite/' , ViewName.ITEM_FAVORITE
    name: 'items:item_favorite'


    """

    """テスト項目
    済 favボタンを押していないユーザーによるfavボタンを押すことでitem.favorite_usersに含まれる要素が1つ増加する *1
    済 favボタンを押していないユーザーによるfavボタンを押すことでitem.favorite_usersに当該ユーザーが追加される *2 
    """

    def setUp(self):
        """テスト環境

        Itemオブジェクト生成用のCategoryオブジェクト作成...category_obj
        Itemオブジェクトに対しFavボタンを押している役のユーザーを作成...fav_user
        Itemオブジェクトを作成した役のユーザーを作成...post_user
        Itemオブジェクト詳細ページにアクセスするユーザーを作成...access_user
        Itemオブジェクトを生成...item_obj1
        fav_userがFavボタンを押しitem_obj1.favorite_users.add()でfav_userが追加される。

        """

        category_obj = Category.objects.create(number="Donar o vender")
        fav_user = User.objects.create_user(username="fav_user", email="fav_test_user@gmail.com", password='12345')
        #fav_user.set_password('12345')
        #fav_user.save()
        post_user = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        #post_user.set_password('12345') #, password='top_secret'
        #post_user.save()
        access_user = User.objects.create_user(username="access_user", email="test_access_user@gmail.com", password='12345')
        #access_user.set_password('12345')
        #access_user.save()
        item_obj1 =  Item.objects.create(user=post_user, id=1, title="テストアイテム１", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        item_obj1.favorite_users.add(fav_user)

    def test_should_add_user_by_push_fab_btn_for_no_fav_user(self):
        # favボタンを押していないユーザーによるfavボタンを押すことでitem.favorite_usersに含まれる要素が1つ増加する *1
        # favボタンを押していないユーザーによるfavボタンを押すことでitem.favorite_usersに当該ユーザーが追加される *2 

        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="access_user", password="12345")
        self.assertTrue(login_status)

        #アクセス前
        response = self.client.get(reverse_lazy(ViewName.ITEM_DETAIL, args=("1",)))
        self.assertTrue("item_obj" in response.context)
        item_obj = response.context["item_obj"]
        self.assertTrue(item_obj.favorite_users.all().count(), 1)

        #Favボタンを押す
        access_user = User.objects.get(username="access_user")
        response = self.client.post(reverse_lazy(ViewName.ITEM_FAVORITE, args="1"), follow=True)
        templates = [ele.name for ele in response.templates]
        #print(templates)
        item_obj = Item.objects.get(id=1)
        self.assertTrue(item_obj.favorite_users.all().count(), 2) # *1
        self.assertTrue(access_user in item_obj.favorite_users.all()) # *2








class ItemDetailTemplatesTest(TestCase):

    """テスト目的
    #ItemDetailViewに使用されるtemplateが正しく使用されているかチェックする

    """

    """テスト対象
    items.views.py ItemDetailView (items:item_detail)

    """

    """テスト項目
    済 未認証ユーザーがアイテム詳細ページにアクセスした場合には使用されるテンプレートは['items/detail_item2.html', 'config/base.html', 'config/include/navbar.html', 'config/include/bottom.html']
    済 アイテム詳細ページの作成者である認証したユーザーがアイテム詳細ページにアクセスした場合には使用されるテンプレートは['items/detail_item2.html', 'config/base.html', 'config/include/navbar.html', 'config/include/bottom.html']
    済 アイテム詳細ページの作成者ではない認証したユーザーがアイテム詳細ページにアクセスした場合には使用されるテンプレートは['items/detail_item2.html', 'config/base.html', 'config/include/navbar.html', 'config/include/bottom.html']
    """

    ITEM_DETAIL_URL_FORMAT = "/items/item/{}/"


    def setUp(self):
        category_obj = Category.objects.create(number="Donar o vender")
        post_user_obj = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        post_user_profile_obj = Profile.objects.get(user=post_user_obj)

        access_user_obj = User.objects.create_user(username="access_user", email="test_access_user@gmail.com", password='12345')
        #access_user_profile_obj = Profile.objects.get(user=access_user_obj)

        solicitud_user_obj = User.objects.create_user(username="solicitud_user", email="test_solicitud_user@gmail.com", password='12345')
        solicitud_user_profile_obj = Profile.objects.get(user=solicitud_user_obj)

        item_obj1 =  Item.objects.create(user=post_user_obj, id=1, title="テストアイテム１", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        dm_obj = DirectMessage.objects.create( owner=post_user_profile_obj, participant=solicitud_user_profile_obj)
        item_obj1.direct_message = dm_obj
        item_obj1.save()

    def test_templates_by_anonymous_user(self):
        """
        未認証ユーザーがアイテム詳細ページにアクセスした場合には使用されるテンプレートは、
        ['items/detail_item2.html', 'config/base.html', 'config/include/navbar.html', 'config/include/bottom.html']
        """
        self.client = Client()
        login_status = self.client.logout()
        self.assertFalse(login_status)  #未認証でアクセス
        url = self.ITEM_DETAIL_URL_FORMAT.format("1")
        response = self.client.get(url)
 
        templates = [ele.name for ele in response.templates]

        self.assertTrue('items/detail_item2.html' in templates)
        self.assertTrue('config/base.html' in templates)
        self.assertTrue('config/include/navbar.html' in templates)
        self.assertTrue('config/include/bottom.html' in templates) 



    def test_templates_by_authentication_and_post_user(self):
        """
        アイテム詳細ページの作成者である認証したユーザーがアイテム詳細ページにアクセスした場合には使用されるテンプレートは、
        ['items/detail_item2.html', 'config/base.html', 'config/include/navbar.html', 'config/include/bottom.html']
        """
        self.client = Client()
        login_status = self.client.login(username="post_user", password='12345')
        self.assertTrue(login_status)  #認証状態でアクセス
        url = self.ITEM_DETAIL_URL_FORMAT.format("1")
        response = self.client.get(url)
 
        templates = [ele.name for ele in response.templates]

        self.assertTrue('items/detail_item2.html' in templates)
        self.assertTrue('config/base.html' in templates)
        self.assertTrue('config/include/navbar.html' in templates)
        self.assertTrue('config/include/bottom.html' in templates)


    def test_templates_by_authentication_no_post_user(self):
        """
        アイテム詳細ページの作成者ではない認証したユーザーがアイテム詳細ページにアクセスした場合には使用されるテンプレートは
        ['items/detail_item2.html', 'config/base.html', 'config/include/navbar.html', 'config/include/bottom.html'] 
        """
        self.client = Client()
        login_status = self.client.login(username="access_user", password='12345')
        self.assertTrue(login_status)  #認証状態でアクセス
        url = self.ITEM_DETAIL_URL_FORMAT.format("1")
        response = self.client.get(url)
 
        templates = [ele.name for ele in response.templates]

        self.assertTrue('items/detail_item2.html' in templates)
        self.assertTrue('config/base.html' in templates)
        self.assertTrue('config/include/navbar.html' in templates)
        self.assertTrue('config/include/bottom.html' in templates)



'''これはItemCreateViewKaizenに置き換えられる
class ItemCreateViewPOSTTest(TestCase):
    """テスト目的
    一定の条件下でのみItemオブジェクトが生成されないように制限する
    """
    """テスト対象
    items/views.py ItemCreateview#POST
    endpoint:"items/'create/"
    name: "items:item_create"
    """
    """テスト項目
    済 category_title_description_adm0_adm1_adm2のデータが有ればItemオブジェクトが生成される
    済 test_categoryデータが不足している場合はFormがinvalidつまりFalseになる
    済 test_categoryデータが不足している場合はItemオブジェクトが作られない
    済 priceデータが不足している場合にはformはinvalidになってしまう
    済 画像データが添付されずに生成されたItemオブジェクトの画像urlはimages_default_images_pngである
    """

    """テストメモ
    ModelFormにModelChiceFieldを実装している。
    このModelChoiceFieldにForeignKeyのオブジェクトを格納するときには
    オブジェクトそのものを渡すのではなくオブジェクト.idで渡すことが必須となる。
    """

    def setUp(self):
        category_obj = Category.objects.create(number="1")
        post_user_obj = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        self.init_data = {}



    def test_category_title_description_adm0_adm1_adm2_priceのデータが有ればItemオブジェクトが生成される(self):
        post_user_obj = User.objects.get(username="post_user")
        profile_obj = Profile.objects.get(user=post_user_obj)
        item_objects_count_before = Item.objects.filter(user=post_user_obj).count()
        category_obj = Category.objects.get(number="1")
        data = {
                'category':category_obj.id, 
                'title':"テスト", 
                'description':"hdahfifif",
                "price":0,
                'adm0':"GUATEMALA",
                'adm1':"Guatemala",
                'adm2':"Guatemala"
                } 
                #'image1':"nin.jpg", 'image2': None, 'image3': None}
        #files = {'image1':mock.MagicMock(spec=File), 'image2': mock.MagicMock(spec=File), 'image3': mock.MagicMock(spec=File)}
        
        form = ItemModelForm(data) #, files
        self.assertTrue(form.is_valid() == True)


        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status)
        response = self.client.post(reverse("items:item_create"), data)
        self.assertEqual(response.status_code, 200)
        item_objects_count_after = Item.objects.filter(user=post_user_obj).count()
        self.assertEqual(item_objects_count_before+1, item_objects_count_after) 


    
    def test_categoryデータが不足している場合はFormがinvalidつまりFalseになる(self):

        data = { 
                'title':"テスト", 
                'description':"hdahfifif", 
                'adm0':"GUATEMALA", 'adm1':"Guatemala",'adm2':"Guatemala", "price":1000
                }

                #'image1':'nini.jpg', 'image2': 'nnin.jpg', 'image3': 'ninli.jpg'
                
        #files = {'image1':mock.MagicMock(spec=File), 'image2': mock.MagicMock(spec=File), 'image3': mock.MagicMock(spec=File)}
        form = ItemModelForm(data)
        self.assertFalse(form.is_valid())



    def test_categoryデータが不足している場合はItemオブジェクトが作られない(self):
        post_user_obj = User.objects.get(username="post_user")
        item_objects_count_before = Item.objects.filter(user=post_user_obj).count()
        data = {
                'title':"テスト", 
                'description':"hdahfifif", 
                'adm0':"GUATEMALA", 'adm1':"Guatemala",'adm2':"Guatemala", "price":1999
                }

        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status)
        response = self.client.post(reverse("items:item_create"), data)
        self.assertEqual(response.status_code, 200)
        item_objects_count_after = Item.objects.filter(user=post_user_obj).count()
        self.assertEqual(item_objects_count_before, item_objects_count_after) 



    def test_priceデータが不足している場合にはformはinvalidになってしまう(self):

        category_obj = Category.objects.get(number="1")
        data = {
        'category': category_obj.id, 
        'title':"テスト", 
        'description':"hdahfifif", 
        'adm0':"GUATEMALA", 'adm1':"Guatemala",'adm2':"Guatemala"
        }

                
        #files = {'image1':mock.MagicMock(spec=File), 'image2': mock.MagicMock(spec=File), 'image3': mock.MagicMock(spec=File)}
        form = ItemModelForm(data)
        self.assertFalse(form.is_valid())



    
    def test_画像データが添付されずに生成されたItemオブジェクトの画像urlはimages_default_item_pngである(self):
        
        post_user_obj = User.objects.get(username="post_user")
        item_objects_count_before = Item.objects.filter(user=post_user_obj).count()
        self.assertEqual(item_objects_count_before, 0)
        category_obj = Category.objects.get(number="1")
        data = {
                'category':category_obj.id, 
                'title':"テスト", 
                'description':"hdahfifif", 
                'adm0':"GUATEMALA", 'adm1':"Guatemala",'adm2':"Guatemala","price":0
                }       
        
        form = ItemModelForm(data)
        self.assertTrue(form.is_valid() )

        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status)
        response = self.client.post(reverse("items:item_create"), data)
        self.assertEqual(response.status_code, 200)
        item_obj = Item.objects.get(user=post_user_obj)
        self.assertEqual(item_obj.image1, "images/default_item.png") 
 '''   
   

class ItemCreateViewKaizenPOSTTest(TestCase):
    """テスト目的
    一定の条件下でのみItemオブジェクトが生成されないように制限する
    """
    """テスト対象
    items/views.py ItemCreateview#POST
    endpoint:"items/'create2/"
    name: "items:item_create"
    """
    """テスト項目
    済 category_title_description_adm0_adm1_adm2のデータが有ればItemオブジェクトが生成される
    済 test_categoryデータが不足している場合はFormがinvalidつまりFalseになる
    済 test_categoryデータが不足している場合はItemオブジェクトが作られない
    済 priceデータが不足している場合にはformはinvalidになってしまう
    済 画像データが添付されずに生成されたItemオブジェクトの画像urlはimages_default_images_pngである
    """

    """テストメモ
    ModelFormにModelChiceFieldを実装している。
    このModelChoiceFieldにForeignKeyのオブジェクトを格納するときには
    オブジェクトそのものを渡すのではなくオブジェクト.idで渡すことが必須となる。
    """

    def setUp(self):
        category_obj = Category.objects.create(number="1")
        post_user_obj = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        self.init_data = {}



    def test_category_title_description_adm0_adm1_adm2_priceのデータが有ればItemオブジェクトが生成される(self):
        post_user_obj = User.objects.get(username="post_user")
        profile_obj = Profile.objects.get(user=post_user_obj)
        item_objects_count_before = Item.objects.filter(user=post_user_obj).count()
        category_obj = Category.objects.get(number="1")
        data = {
                'category':category_obj.id, 
                'title':"テスト", 
                'description':"hdahfifif",
                "price":0,
                'adm0':"GUATEMALA",
                'adm1':"Guatemala",
                'adm2':"Guatemala"
                } 
                #'image1':"nin.jpg", 'image2': None, 'image3': None}
        #files = {'image1':mock.MagicMock(spec=File), 'image2': mock.MagicMock(spec=File), 'image3': mock.MagicMock(spec=File)}
        
        form = ItemModelForm(data) #, files
        self.assertTrue(form.is_valid() == True)


        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status)
        response = self.client.post(reverse(ViewName.ITEM_CREATE), data)
        self.assertEqual(response.status_code, 200)
        item_objects_count_after = Item.objects.filter(user=post_user_obj).count()
        self.assertEqual(item_objects_count_before+1, item_objects_count_after) 


    
    def test_categoryデータが不足している場合はFormがinvalidつまりFalseになる(self):

        data = { 
                'title':"テスト", 
                'description':"hdahfifif", 
                'adm0':"GUATEMALA", 'adm1':"Guatemala",'adm2':"Guatemala", "price":1000
                }

                #'image1':'nini.jpg', 'image2': 'nnin.jpg', 'image3': 'ninli.jpg'
                
        #files = {'image1':mock.MagicMock(spec=File), 'image2': mock.MagicMock(spec=File), 'image3': mock.MagicMock(spec=File)}
        form = ItemModelForm(data)
        self.assertFalse(form.is_valid())



    def test_categoryデータが不足している場合はItemオブジェクトが作られない(self):
        post_user_obj = User.objects.get(username="post_user")
        item_objects_count_before = Item.objects.filter(user=post_user_obj).count()
        data = {
                'title':"テスト", 
                'description':"hdahfifif", 
                'adm0':"GUATEMALA", 'adm1':"Guatemala",'adm2':"Guatemala", "price":1999
                }

        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status)
        #response = self.client.post(reverse("items:item_create"), data)
        response = self.client.post(reverse(ViewName.ITEM_CREATE), data)
        self.assertEqual(response.status_code, 200)
        item_objects_count_after = Item.objects.filter(user=post_user_obj).count()
        self.assertEqual(item_objects_count_before, item_objects_count_after) 



    def test_priceデータが不足している場合にはformはinvalidになってしまう(self):

        category_obj = Category.objects.get(number="1")
        data = {
        'category': category_obj.id, 
        'title':"テスト", 
        'description':"hdahfifif", 
        'adm0':"GUATEMALA", 'adm1':"Guatemala",'adm2':"Guatemala"
        }

                
        #files = {'image1':mock.MagicMock(spec=File), 'image2': mock.MagicMock(spec=File), 'image3': mock.MagicMock(spec=File)}
        form = ItemModelForm(data)
        self.assertFalse(form.is_valid())



    
    def test_画像データが添付されずに生成されたItemオブジェクトの画像urlはimages_default_item_pngである(self):
        
        post_user_obj = User.objects.get(username="post_user")
        item_objects_count_before = Item.objects.filter(user=post_user_obj).count()
        self.assertEqual(item_objects_count_before, 0)
        category_obj = Category.objects.get(number="1")
        data = {
                'category':category_obj.id, 
                'title':"テスト", 
                'description':"hdahfifif", 
                'adm0':"GUATEMALA", 'adm1':"Guatemala",'adm2':"Guatemala","price":0
                }       
        
        form = ItemModelForm(data)
        self.assertTrue(form.is_valid() )

        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status)
        response = self.client.post(reverse(ViewName.ITEM_CREATE), data)
        self.assertEqual(response.status_code, 200)
        item_obj = Item.objects.get(user=post_user_obj)
        self.assertEqual(item_obj.image1, "images/default_item.png")  

    







