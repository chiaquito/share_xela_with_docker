from django.test import TestCase
from django.test import Client
from django.urls import reverse, reverse_lazy

from config.constants import ViewName
from config.constants import TemplateName

from categories.models import Category
from direct_messages.models import DirectMessage
from items.models import Item
from django.contrib.auth.models import User

from profiles.models import Profile
from solicitudes.models import Solicitud

from solicitudes.forms import SolicitudModelForm

import random
from config.tests.utils import *


#testを書く


class SolicitudInputViewGETMethodTest(TestCase):
    """テスト目的
    アイテム詳細ページの申請ボタンを押すと、メッセージフォームを表示する機能を担保する

    """
    """テスト対象
    endpont: "solicitudes/item/<int:pk>/"
    name: "solicitudes:solicitud_input"
    Get methodのみ
    """
    """テスト項目
    済 未認証ユーザーによるアクセスの場合には、認証ページにリダイレクトされる*1
    済 記事作成者でかつ認証したユーザーのアクセスの場合には、homeにリダイレクトされる*2
    済 認証ユーザーかつ記事作成者以外のアクセスの場合には"solicitudes/input_form.html"テンプレートが表示される。*3
    済 認証ユーザーかつ記事作成者以外のアクセスの場合にはcontextにキー"item_obj"が存在する*4
    済 認証ユーザーかつ記事作成者以外のアクセスの場合にはendpointに含まれるintに従って該当するidの記事が表示される。*5
    済 認証ユーザーかつ記事作成者以外のアクセスの場合にはcontextにキー"form"が存在する*6
    済 認証ユーザーかつ記事作成者以外のアクセスの場合にはcontextの"form"は"message"の項目がある*7    
    """
    def setUp(self):
        """テスト環境
        Itemオブジェクト生成のためのCategoryオブジェクトを生成する...category_obj
        Itemオブジェクト生成のためのUserオブジェクトを生成する...post_user_obj
        Itemオブジェクトを生成する...item_obj1
        DMオブジェクト生成のためにProfileオブジェクトを取得する...post_user_profile_obj
        取引相手としてUserオブジェクトを生成する...participant
        DMオブジェクト生成のためにProfileオブジェクトを取得する...participant_profile_obj
        DMオブジェクトを生成する...dm_obj
        DMオブジェクトに関連のないUserオブジェクトを作成する...acces_user_obj
        適切なformデータを生成する
        #不適切なformデータを生成する
        """
        
        self.category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_user_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))
        participant, participant_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="test_participant"))
        acces_user_obj, acces_user_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="access_user"))
        item_obj1 = create_item_for_test(user_obj=post_user_obj, item_data=create_item_data(category_obj=self.category_obj))
        self.item_obj1 = item_obj1
        solicitud_obj = create_solicitud_for_test(item_obj1, participant, create_solicitud_data())
        dm_obj = create_direct_message_for_test(solicitud_obj)

        

    def test_should_redirect_auth_for_anonymous_user(self):
        #未認証ユーザーによるアクセスの場合には、認証ページにリダイレクトされる*1
        self.client = Client()
        login_status = self.client.logout()
        self.assertFalse(login_status) #未認証状態でアクセス
        response = self.client.get(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj1.id,)), follow=True)
        self.assertTrue('account/login.html' in get_templates_by_response(response)) #*1


    def test_should_redirect_home_for_post_user(self):
        #記事作成者でかつ認証したユーザーのアクセスの場合には、homeにリダイレクトされる*2
        self.client = Client()
        login_status = self.client.login(username="post_user", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行
        response = self.client.get(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj1.id,)), follow=True)
        self.assertTrue(TemplateName.HOME in get_templates_by_response(response)) #*2


    def test_should_show_input_form_html_for_authenticated_user(self):
        #認証ユーザーかつ記事作成者以外のアクセスの場合には"solicitudes/input_form.html"テンプレートが表示される。*3
        self.client = Client()
        login_status = self.client.login(username="access_user", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行
        response = self.client.get(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj1.id,)), follow=True)
        self.assertTrue(TemplateName.SOLICITUD_INPUT in get_templates_by_response(response)) #*3


    def test_should_exist_item_obj_of_context_key(self):
        #認証ユーザーかつ記事作成者以外のアクセスの場合にはcontextにキー"item_obj"が存在する*4
        #認証ユーザーかつ記事作成者以外のアクセスの場合にはendpointに含まれるintに従って該当するidの記事が表示される。*5
        #認証ユーザーかつ記事作成者以外のアクセスの場合にはcontextにキー"form"が存在する*6
        #認証ユーザーかつ記事作成者以外のアクセスの場合にはcontextの"form"は"message"の項目がある*7 

        post_user_obj = User.objects.get(username="post_user")
        create_item_for_test(post_user_obj, create_item_data(self.category_obj))
        create_item_for_test(post_user_obj, create_item_data(self.category_obj))

        self.client = Client()
        login_status = self.client.login(username="access_user", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行
        response = self.client.get(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj1.id,)), follow=True)
        self.assertTrue("item_obj" in response.context) #*4
        item_obj = response.context["item_obj"]
        self.assertTrue(item_obj.id, 1) #*5
        self.assertTrue("form" in response.context) #*6
        form = response.context["form"]
        self.assertTrue("message" in form.fields.keys())#*7 




class SolicitudInputViewPOSTMethodTest(TestCase):
    """テスト目的
    メッセージフォームに入力されたデータをもとにSolicitudオブジェクトを生成する機能を担保する

    """
    """テスト対象
    endpont: "solicitudes/item/<int:pk>/"
    name: "solicitudes:solicitud_input"
    Post methodのみ
    """
    """テスト項目
    済 未認証ユーザーによるアクセスの場合には、認証ページにリダイレクトされる *1
    済 記事作成者でかつ認証したユーザーのアクセスの場合には、homeにリダイレクトされる *2
    保留 formの内容が不適切であればSolicitudオブジェクトは生成されない *3
    保留 formの内容が不適切であれば"solicitudes/input_form.html"テンプレートが表示される。 *4
    formの内容が適切であればSolicitudオブジェクトが新たに1つ生成される *5
    formの内容が適切であればItem詳細ページが表示される。 *6
    新たに生成されたSolicitudオブジェクトのapplicant値はアクセスユーザーのProfileオブジェクトである。 *7
    新たに生成されたSolicitudオブジェクトはintに対応するid値をもつItemオブジェクトのsolicitudesに含まれる。 *8
    """
    def setUp(self):
        """テスト環境
        Itemオブジェクト生成のためのCategoryオブジェクトを生成する...category_obj
        Itemオブジェクト生成のためのUserオブジェクトを生成する...post_user_obj
        Itemオブジェクトを生成する...item_obj1
        DMオブジェクト生成のためにProfileオブジェクトを取得する...post_user_profile_obj
        取引相手としてUserオブジェクトを生成する...participant
        DMオブジェクト生成のためにProfileオブジェクトを取得する...participant_profile_obj
        DMオブジェクトを生成する...dm_obj
        DMオブジェクトに関連のないUserオブジェクトを作成する...acces_user_obj
        適切なformデータを生成する
        #不適切なformデータを生成する
        """
        category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_user_profile_obj =  create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))
        self.item_obj1 = create_item_for_test(post_user_obj, create_item_data(category_obj))
        participant, participant_profile_obj =  create_user_for_test(create_user_data(prefix_user_emailaddress="participant"))
        solicitud_obj = create_solicitud_for_test(self.item_obj1, participant, create_solicitud_data())
        dm_obj = create_direct_message_for_test(solicitud_obj)
        acces_user_obj, acces_user_profile_obj =  create_user_for_test(create_user_data(prefix_user_emailaddress="access_user"))
        self.item_obj3 = create_item_for_test(post_user_obj, create_item_data(category_obj))


    def test_should_redirect_to_auth_for_anonymous_user(self):
        # 未認証ユーザーによるアクセスの場合には、認証ページにリダイレクトされる *1
        self.client = Client()
        login_status = self.client.logout()
        self.assertFalse(login_status) #未認証状態でアクセス
        data = {"message":"ばばば"}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj1.id,) ),data, follow=True)
        templates = [ele.name for ele in response.templates]
        self.assertTrue('account/login.html' in templates) #*1

    def test_should_redirect_home_for_post_user(self):
        #記事作成者でかつ認証したユーザーのアクセスの場合には、homeにリダイレクトされる*2
        self.client = Client()
        login_status = self.client.login(username="post_user", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行
        data = {"message":"ばばば"}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj1.id,)),data, follow=True)
        templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.HOME in templates) #*2
 
    """
    formの不適切な内容が見つからない。blankはhtmlでバリデーション
    def test_sasasa(self):
        # formの内容が不適切であればSolicitudオブジェクトは生成されない *3
        self.client = Client()
        login_status = self.client.login(username="post_user", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行
        data = {"message":""}
        form = SolicitudModelForm(data)

        self.assertTrue(form.is_valid())

        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args="1"),data, follow=True)
        templates = [ele.name for ele in response.templates]
        #self.assertTrue(TemplateName.HOME in templates) #*2
    """

    def test_should_create_an_instance(self):
        # formの内容が適切であればSolicitudオブジェクトが新たに1つ生成される *5
        # formの内容が適切であればItem詳細ページが表示される。 *6
        # 新たに生成されたSolicitudオブジェクトのapplicant値はアクセスユーザーのProfileオブジェクトである。 *7
        # 新たに生成されたSolicitudオブジェクトはintに対応するid値をもつItemオブジェクトのsolicitudesに含まれる。 *8
        before_solicitudes_count = Solicitud.objects.all().count()
        self.client = Client()
        access_user = User.objects.get(username="access_user")
        access_user_profile = Profile.objects.get(user=access_user)
        login_status = self.client.login(username="access_user", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行
        data = {"message":"sadcscv"}
        form = SolicitudModelForm(data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj3.id,)),data, follow=True)
        #templates = [ele.name for ele in response.templates]
        #self.assertTrue(TemplateName.HOME in templates) #*2
        after_solicitudes_count = Solicitud.objects.all().count()
        self.assertTrue(after_solicitudes_count, before_solicitudes_count+1) #*5
        item_obj = response.context["item_obj"]
        self.assertTrue(item_obj.id, self.item_obj3.id) #*6
        templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.ITEM_DETAIL in templates) #*6
        solicitud_obj = Item.objects.get(id=self.item_obj3.id).solicitudes.all().order_by("id").last()
        self.assertEqual(solicitud_obj.applicant, access_user_profile) #*7
        self.assertTrue(solicitud_obj, item_obj.solicitudes.all()) # *8


class SolicitudListViewTest(TestCase):
    """テスト目的
    """
    """テスト対象
    solicitudes.views.py SolicitudListView
    endpoint: "solicitudes/item/<int:pk>/solicitud_list/"
    name: "solicitudes:solicitud_list"
    """
    """テスト項目

    未認証ユーザーによるアクセスの場合には、認証ページにリダイレクトする *1
    リクエストユーザーが記事作成者ではない場合にはHomeにリダイレクトする *2

    Itemオブジェクトのsolicitudesに含まれるSolicitudオブジェクトのうち一つがaccepted==Trueの場合にはDM詳細ページにリダイレクトされる *3
    contextに"solicitudes_objects"が存在する *4
    Itemオブジェクトのsolicitudesに含まれるSolicitudオブジェクトがもれなく適切に表示されている。 *5
    contextに"item_obj"が存在する *6  
    """
    def setUp(self):
        """テスト環境
        Itemオブジェクト生成のためのCategoryオブジェクトを生成する...category_obj
        Itemオブジェクト生成のためのUserオブジェクトを生成する...post_user_obj
        Itemオブジェクトを生成する...item_obj1
        DMオブジェクト生成のためにProfileオブジェクトを取得する...post_user_profile_obj
        取引相手としてUserオブジェクトを生成する...participant
        DMオブジェクト生成のためにProfileオブジェクトを取得する...participant_profile_obj
        DMオブジェクトを生成する...dm_obj
        DMオブジェクトに関連のないUserオブジェクトを作成する...acces_user_obj
        適切なformデータを生成する
        #不適切なformデータを生成する
        """

        category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_user_profile_obj =  create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))
        self.item_obj1 = create_item_for_test(post_user_obj, create_item_data(category_obj))
        participant, participant_profile_obj =  create_user_for_test(create_user_data(prefix_user_emailaddress="participant"))
        acces_user_obj, acces_user_profile_obj =  create_user_for_test(create_user_data(prefix_user_emailaddress="access_user"))
        acces_user_obj1, acces_user_profile_obj1 =  create_user_for_test(create_user_data(prefix_user_emailaddress="access_user1"))
        acces_user_obj2, acces_user_profile_obj2 =  create_user_for_test(create_user_data(prefix_user_emailaddress="access_user2"))
        self.item_obj3 = create_item_for_test(post_user_obj, create_item_data(category_obj))
        

    def test_should_redirect_to_auth_for_anonymous_user(self):
        # 未認証ユーザーによるアクセスの場合には、認証ページにリダイレクトされる *1
        self.client = Client()
        login_status = self.client.logout()
        self.assertFalse(login_status) #未認証状態でアクセス
        #data = {"message":"ばばば"}
        response = self.client.get(reverse_lazy(ViewName.SOLICITUD_LIST, args=(self.item_obj1.id,)), follow=True)
        templates = [ele.name for ele in response.templates]
        self.assertTrue('account/login.html' in templates) #*1

    def test_should_redirect_home_for_post_user(self):
        #記事作成者以外でかつ認証したユーザーのアクセスの場合には、homeにリダイレクトされる*2
        self.client = Client()
        login_status = self.client.login(username="access_user", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行
        #data = {"message":"ばばば"}
        response = self.client.get(reverse_lazy(ViewName.SOLICITUD_LIST, args=(self.item_obj1.id,)), follow=True)
        templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.HOME in templates) #*2

    def test_should_redirect_dm_for_authenticated_post_user(self):
        # Itemオブジェクトのsolicitudesに含まれるSolicitudオブジェクトのうち一つがaccepted==Trueの場合にはDM詳細ページにリダイレクトされる *3

        self.client = Client()
        access_user = User.objects.get(username="access_user")
        #access_user_profile = Profile.objects.get(user=access_user)
        login_status = self.client.login(username="access_user", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行
        data = {"message":"sadcscv"}
        form = SolicitudModelForm(data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj3.id,)),data, follow=True) #Solicitudオブジェクトを生成
        solicitud_obj = Item.objects.get(id=self.item_obj3.id).solicitudes.all().order_by("id").last()
        solicitud_obj.accepted = True
        solicitud_obj.save()

        self.client = Client()
        access_user = User.objects.get(username="post_user")
        #access_user_profile = Profile.objects.get(user=access_user)
        login_status = self.client.login(username="access_user", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行 
        response = self.client.get(reverse_lazy(ViewName.SOLICITUD_LIST, args=(self.item_obj3.id,)), follow=True)
        templates = [ele.name for ele in response.templates]       
        self.assertTrue("direct_messages/dm_detail.html" in templates)


    def test_should_redirect_dm_for_authenticated_post_user(self):
        # contextに"solicitudes_objects"が存在する *4
        # Itemオブジェクトのsolicitudesに含まれるSolicitudオブジェクトがもれなく適切に表示されている。 *5
        # contextに"item_obj"が存在する *6  

        self.client = Client()
        #access_user = User.objects.get(username="access_user")
        #access_user_profile = Profile.objects.get(user=access_user)
        login_status = self.client.login(username="access_user", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行
        data = {"message":"sadcscv"}
        form = SolicitudModelForm(data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj3.id,)),data, follow=True) #Solicitudオブジェクトを生成

        self.client = Client()
        #access_user = User.objects.get(username="access_user2")
        #access_user_profile = Profile.objects.get(user=access_user)
        login_status = self.client.login(username="access_user1", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行
        data = {"message":"sadcscv"}
        form = SolicitudModelForm(data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj3.id,)),data, follow=True) #Solicitudオブジェクトを生成

        self.client = Client()
        #access_user = User.objects.get(username="access_user2")
        #access_user_profile = Profile.objects.get(user=access_user)
        login_status = self.client.login(username="access_user2", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行
        data = {"message":"sadcscv"}
        form = SolicitudModelForm(data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj3.id,)),data, follow=True) #Solicitudオブジェクトを生成


        self.client = Client()
        #access_user = User.objects.get(username="post_user")
        #access_user_profile = Profile.objects.get(user=access_user)
        login_status = self.client.login(username="post_user", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセスを実行 
        response = self.client.get(reverse_lazy(ViewName.SOLICITUD_LIST, args=(self.item_obj3.id,)), follow=True)
        templates = [ele.name for ele in response.templates]
        #print(templates)       
        self.assertTrue('solicitudes/solicitud_decision.html' in templates)
        self.assertTrue("solicitudes_objects" in response.context) # *4
        self.assertTrue("item_obj" in response.context) # *6  
        solicitudes_objects = Item.objects.get(id=self.item_obj3.id).solicitudes.all()

        self.assertTrue(response.context["solicitudes_objects"], solicitudes_objects ) # *5


class SolicitudSelectViewTest(TestCase):
    """テスト目的/担保される項目
    記事作成者が取引相手を選択したらDirectMessageオブジェクトが生成される。
    記事作成者が取引相手を選択したらSolicitudオブジェクトのaccepted値がTrueに変更される
    記事作成者が取引相手を選択したらDM詳細ページにリダイレクトされる。

    """
    """テスト対象
    SolicitudSelectView
    endpoint: "solicitudes/solicitud/<int:pk>/select/"
    name: "solicitudes:solicitud_decision"
    """
    """テスト項目
    済 記事作成者が取引相手を選択したらDirectMessageオブジェクトが生成される。*0
    済 urlのintに合致するid値をもつSolicitudオブジェクトのaccepted値がTrueに変更される *1
    済 DM詳細ページにリダイレクトされる。 *2
    """
    def setUp(self):
        """テスト環境
        Itemオブジェクト生成のためのCategoryオブジェクトを生成する...category_obj
        Itemオブジェクト生成のためのUserオブジェクトを生成する...post_user_obj
        Itemオブジェクトを生成する...item_obj1
        DMオブジェクト生成のためにProfileオブジェクトを取得する...post_user_profile_obj
        取引相手としてUserオブジェクトを生成する...participant
        DMオブジェクト生成のためにProfileオブジェクトを取得する...participant_profile_obj
        DMオブジェクトを生成する...dm_obj
        DMオブジェクトに関連のないUserオブジェクトを作成する...acces_user_obj
        適切なformデータを生成する
        #不適切なformデータを生成する
        """



        category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_user_profile_obj =  create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))        
        self.item_obj1 = create_item_for_test(post_user_obj, create_item_data(category_obj))
        participant, participant_profile_obj     =  create_user_for_test(create_user_data(prefix_user_emailaddress="participant"))
        acces_user_obj,  access_user_profile_obj =  create_user_for_test(create_user_data(prefix_user_emailaddress="access_user"))
        acces_user_obj1, access_user_profile_obj =  create_user_for_test(create_user_data(prefix_user_emailaddress="access_user1"))
        acces_user_obj2, access_user_profile_obj =  create_user_for_test(create_user_data(prefix_user_emailaddress="access_user2"))

 
    def test_change_accepted_to_true_by_select_solicitud(self):
        #urlのintに合致するid値をもつSolicitudオブジェクトのaccepted値がTrueに変更される *1
        
        #最初にsolicitudオブジェクトの作成(取引の申請)
        self.client = Client()
        login_status = self.client.login(username="access_user", password="1234tweet")
        self.assertTrue(login_status)
        data = {"message":"jcsiovjso"}
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj1.id,)), data, follow=True)
        #記事作成者が取引相手を決定(SolicitudSelectViewの実行)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="1234tweet")
        self.assertTrue(login_status)
        solicitud_id = Item.objects.get(id=self.item_obj1.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)
        solicitud_obj = Item.objects.get(id=self.item_obj1.id).solicitudes.all().first()
        self.assertTrue(solicitud_obj.accepted)
        solicitud_obj = Solicitud.objects.get(id=solicitud_id)
        self.assertTrue(solicitud_obj.accepted) # *1



    def test_create_DirectMessage_object_by_select_solicitud(self):
        # 記事作成者が取引相手を選択したらDirectMessageオブジェクトが生成される。*0

        #最初にsolicitudオブジェクトの作成(取引の申請)
        self.client = Client()
        login_status = self.client.login(username="access_user", password="1234tweet")
        self.assertTrue(login_status)
        data = {"message":"jcsiovjso"}
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj1.id,)), data, follow=True)
        
        #記事作成者が取引相手を決定(SolicitudSelectViewの実行)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="1234tweet")
        self.assertTrue(login_status)
        solicitud_id = Item.objects.get(id=self.item_obj1.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)
        dm_exist = Item.objects.get(id=self.item_obj1.id).direct_message
        #print("dm_exist")
        #print(dm_exist)
        self.assertTrue(dm_exist != None) #*0
        dm_obj = response.context["dm_obj"]
        #print(dm_obj)
        self.assertTrue(dm_obj != None) #*0


    def test_redirect_DirectMessage_detail_by_select_solicitud(self):
        # DM詳細ページにリダイレクトされる。 *2

        #最初にsolicitudオブジェクトの作成(取引の申請)
        self.client = Client()
        login_status = self.client.login(username="access_user", password="1234tweet")
        self.assertTrue(login_status)
        data = {"message":"jcsiovjso"}
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(self.item_obj1.id,)), data, follow=True)
        
        #記事作成者が取引相手を決定(SolicitudSelectViewの実行)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="1234tweet")
        self.assertTrue(login_status)
        solicitud_id = Item.objects.get(id=self.item_obj1.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)

        templates = [ele.name for ele in response.templates]
        self.assertTrue("direct_messages/dm_detail.html" in templates) #*2





