from django.test import TestCase, Client
from django.urls import resolve, reverse, reverse_lazy

# Create your tests here.

from config.constants import ViewName, TemplateName

from feedback.models import Feedback
from feedback.views import FeedbackView
from feedback.forms import FeedbackModelForm

from django.contrib.auth.models import User
from categories.models import Category
from items.models import Item
from direct_messages.models import DirectMessage, DirectMessageContent
from favorite.models        import Favorite
from profiles.models        import Profile
from solicitudes.models     import Solicitud




class DirectMessageDetailViewGETTest(TestCase):

    """テスト目的
    DMオブジェクトを参照するページを表示するDirectMessageDetailViewに
    未認証ユーザーor DMオブジェクトに関連しないユーザーは閲覧できないことを担保する。
    またDirectMessageの状態によってcontext["btn_feedback"]を表示するか否かの挙動の正確性を担保する
    """

    """テスト対象
    direct_messages/views.py DirectMessageDetailView#GET
    endpoint: direct_messages/<int:pk>/
    name: 'direct_messages:dm_detail'
    """

    """テスト項目
    済 未認証ユーザーによるアクセスはhomeにredirectする*1
    済 未認証ユーザーによるアクセスの場合、context['dm_obj']が存在する。*21
    済 未認証ユーザーによるアクセスの場合、context['dm_content_objects']が存在する。*22
    済 未認証ユーザーによるアクセスの場合、context['form']が存在する。*23
    済 認証ユーザー(participant, post_user)によるアクセスの場合、context['dm_obj']が存在する。*2
    済 認証ユーザー(participant, post_user)によるアクセスの場合、context['dm_content_objects']が存在する。*3
    済 認証ユーザー(participant, post_user)によるアクセスの場合、context['form']が存在する。*4
    済 認証ユーザー(DirectMessageオブジェクトに関係ないユーザー)によるアクセスの場合、context['dm_obj']が存在しない。*a1
    済 認証ユーザー(DirectMessageオブジェクトに関係ないユーザー)によるアクセスの場合、context['dm_content_objects']が存在しない。*a2
    済 認証ユーザー(DirectMessageオブジェクトに関係ないユーザー)によるアクセスの場合、context['form']が存在しない。*a3 
    済 認証ユーザー(DirectMessageオブジェクトに関係ないユーザー)によるアクセスの場合、HOMEにリダイレクトされる。*a4    
    済 DirectMessageオブジェクトのownerである認証ユーザーによるアクセスの場合でDirectMessage.is_feedbacked_by_ownerがTrueの場合context["btn_feedback"]が存在しない *5
    済 DirectMessageオブジェクトのownerである認証ユーザーによるアクセスの場合でDirectMessage.is_feedbacked_by_ownerがFalseの場合context["btn_feedback"]が存在する *6
    済 DirectMessageオブジェクトのpartipantである認証ユーザーによるアクセスの場合でDirectMessage.is_feedbacked_by_partipantがTrueの場合context["btn_feedback"]が存在しない *7
    済 DirectMessageオブジェクトのpartipantである認証ユーザーによるアクセスの場合でDirectMessage.is_feedbacked_by_partipantがFalseの場合context["btn_feedback"]が存在する *8
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
        category_obj = Category.objects.create(number="Donar o vender")
        post_user_obj = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        item_obj1 =  Item.objects.create(user=post_user_obj, id=1, title="テストアイテム１", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        post_user_profile_obj = Profile.objects.get(user=post_user_obj)
        participant = User.objects.create_user(username="participant", email="test_participant@gmail.com", password='12345')
        participant_profile_obj = Profile.objects.get(user=participant)
        #dm_obj = DirectMessage.objects.create(id=2, owner=post_user_profile_obj, participant=participant_profile_obj)
        acces_user_obj = User.objects.create_user(username="access_user", email="test_access_user@gmail.com", password='12345')
        self.valid_form_data = {"content":"良かった", "level":2}
        


    def test_should_redirect_home_for_anonymous_user(self):
        # 未認証ユーザーによるアクセスはhomeにredirectする*1
        # 未認証ユーザーによるアクセスの場合、context['dm_obj']が存在する。*21
        # 未認証ユーザーによるアクセスの場合、context['dm_content_objects']が存在する。*22
        # 未認証ユーザーによるアクセスの場合、context['form']が存在する。*23
        self.client = Client()
        login_status = self.client.logout()
        self.assertFalse(login_status) #未認証状態でアクセスを行う
        response = self.client.get(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL,  args="2"), follow=True)
        self.assertFalse('dm_obj' in response.context) #*21
        self.assertFalse('dm_content_objects' in response.context) #*22
        self.assertFalse('form' in response.context) # *23
        templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.HOME in templates) #HOMEにリダイレクトされる *1


    def test_should_exist_dm_obj_ContextKey_for_Participant(self):
        # 認証ユーザー(participant)によるアクセスの場合、context['dm_obj']が存在する。*2
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=str(item_obj.id)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=str(solicitud_id)), data, follow=True)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status)
        dm_id = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.get(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=str(dm_id)), follow=True)
        self.assertTrue("dm_obj" in response.context) #*2


    def test_should_exist_dm_content_objects_ContextKey_for_Participant(self):
        # 認証ユーザー(participant)によるアクセスの場合、context['dm_content_objects']が存在する。*3
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=str(item_obj.id)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=str(solicitud_id)), data, follow=True)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status)
        dm_id = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.get(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=str(dm_id)), follow=True)
        self.assertTrue("dm_content_objects" in response.context) #*3  


    def test_should_exist_form_ContextKey_for_Participant(self):
        # 認証ユーザー(participant)によるアクセスの場合、context['form']が存在する。*4
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(str(item_obj.id),)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status)
        dm_id = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.get(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=(str(dm_id),)), follow=True)
        self.assertTrue("form" in response.context) #*4


    def test_should_exist_dm_obj_ContextKey_for_Post_user(self):
        # 認証ユーザー(記事作成者)によるアクセスの場合、context['dm_obj']が存在する。*2
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=str(item_obj.id)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=str(solicitud_id)), data, follow=True)
        self.assertTrue("dm_obj" in response.context) #*2


    def test_should_exist_dm_content_objects_ContextKey_for_Post_user(self):
        # 認証ユーザー(post_user記事作成者)によるアクセスの場合、context['dm_content_objects']が存在する。*3
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=str(item_obj.id)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=str(solicitud_id)), data, follow=True)
        self.assertTrue("dm_content_objects" in response.context) #*3


    def test_should_exist_form_ContextKey_for_Post_user(self):
        # 認証ユーザー(post_user記事作成者)によるアクセスの場合、context['form']が存在する。*4
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=str(item_obj.id)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)
        self.assertTrue("form" in response.context) #*4


    def test_not_should_exist_dm_obj_ContextKey_for_access_user(self):
        # 認証ユーザー(DirectMessageオブジェクトに関係ないユーザー)によるアクセスの場合、context['dm_obj']が存在しない。*a1
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=str(item_obj.id)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=str(solicitud_id)), data, follow=True)

        self.client = Client()
        login_status = self.client.login(username="access_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        dm_id = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.get(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=str(dm_id)), follow=True)
        self.assertTrue("dm_obj" not in response.context) #*a1


    def test_not_should_exist_dm_content_objects_ContextKey_for_access_user(self):
        # 認証ユーザー(DirectMessageオブジェクトに関係ないユーザー)によるアクセスの場合、context['dm_obj']が存在しない。*a2
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=str(item_obj.id)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)

        self.client = Client()
        login_status = self.client.login(username="access_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        dm_id = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.get(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=str(dm_id)), follow=True)
        self.assertTrue("dm_content_objects" not in response.context) #*a2


    def test_not_should_exist_form_ContextKey_for_access_user(self):
        # 認証ユーザー(DirectMessageオブジェクトに関係ないユーザー)によるアクセスの場合、context['form']が存在しない。*a3
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=str(item_obj.id)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)

        self.client = Client()
        login_status = self.client.login(username="access_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        dm_id = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.get(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=(str(dm_id),)), follow=True)
        self.assertTrue("form" not in response.context) #*a3



    def test_should_redirect_HOME_for_access_user(self):
        # 認証ユーザー(DirectMessageオブジェクトに関係ないユーザー)によるアクセスの場合、HOMEにリダイレクトされる。*a4
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(str(item_obj.id),)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)

        self.client = Client()
        login_status = self.client.login(username="access_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        dm_id = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.get(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=(str(dm_id),)), follow=True)
        templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.HOME in templates) #*a4



    def test_should_not_exist_btn_feedback_ContextKey_when_is_feedbacked_by_owner_True_for_owner(self):
        # DirectMessageオブジェクトのownerである認証ユーザーによるアクセスの場合でDirectMessage.is_feedbacked_by_ownerがTrueの場合context["btn_feedback"]が存在しない *5
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(str(item_obj.id),)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)
        #post_user(記事作成者)がfeedbackを作成する
        data = {"content":"djfjsgso", "level":1}
        form = FeedbackModelForm(data)
        self.assertTrue(form.is_valid())        
        self.client.session["dm_obj_pk"] = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.post(reverse_lazy(ViewName.FEEDBACK_CREATE), follow=True)
        self.assertTrue("btn_feedback" not in response.context) # *5


    def test_should_exist_btn_feedback_ContextKey_when_is_feedbacked_by_owner_False_for_owner(self):
        # DirectMessageオブジェクトのownerである認証ユーザーによるアクセスの場合でDirectMessage.is_feedbacked_by_ownerがTrueの場合context["btn_feedback"]が存在しない *5
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(str(item_obj.id),)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)
        #post_user(記事作成者)がfeedbackを作成するとTrueに変わってしまうのでfeedbackは作成しない
        dm_obj_id = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.get(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=(str(dm_obj_id),)),  follow=True)
        self.assertTrue("btn_feedback" in response.context) #*6


    def test_should_not_exist_btn_feedback_ContextKey_when_is_feedbacked_by_participant_True_for_Participant(self):
        # DirectMessageオブジェクトのownerである認証ユーザーによるアクセスの場合でDirectMessage.is_feedbacked_by_ownerがTrueの場合context["btn_feedback"]が存在しない *5
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(str(item_obj.id),)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)
        #とTrueにするためにparticipantがfeedbackを作成する
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status)
        data = {"content":"djfjsgso", "level":1}
        form = FeedbackModelForm(data)
        self.assertTrue(form.is_valid()) #フォーム内容が適切かチェック
        self.client.session["dm_obj_pk"] = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.post(reverse_lazy(ViewName.FEEDBACK_CREATE), data, follow=True)
        self.assertTrue("btn_feedback" not in response.context) #*7


    def test_should_exist_btn_feedback_ContextKey_when_is_feedbacked_by_participant_False_for_Participant(self):
        # DirectMessageオブジェクトのownerである認証ユーザーによるアクセスの場合でDirectMessage.is_feedbacked_by_ownerがTrueの場合context["btn_feedback"]が存在しない *5
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(str(item_obj.id),)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)
        
        #participantがfeedbackを作成するとTrueになってしまうのでfeedbackを作成しない
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status)
        dm_obj_id = Item.objects.get(id=item_obj.id).direct_message.id
        self.client.session["dm_obj_pk"] = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.get(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=(str(dm_obj_id),)), follow=True)
        self.assertTrue("btn_feedback" in response.context) # *8








class DirectMessageDetailViewPOSTTest(TestCase):
    """テスト目的
    DirectMessageContentインスタンスを生成するメソッド。生成後は再度DirectMessageContentの一覧を表示させる機能を担保する
    """
    """テスト対象
    direct_messages/views.py DirectMessageDetailView#post

    endpoint: direct_messages/<int:pk>/
    name: 'direct_messages:dm_detail'    
    """
    """テスト項目
    済 未認証ユーザーのアクセスの場合HOMEにリダイレクトする。*1
    済 アクセスユーザーがDirectMessageに関連しないユーザー(owner, participantではないユーザー)の場合HOMEにリダイレクトする。*2
    endpoint送信後、formが適切であればDirectMassageContentが一つ生成される。*3
    endpoint送信後、formが適切であればDirectMassageContentがDirectMessageに加えられる。*4
    endpoint送信後、formが適切であればDM詳細ページにリダイレクトされる*5

    """
    def setUp(self):
        """テスト環境
        Itemオブジェクト生成のためのCategoryオブジェクトを生成する...category_obj
        Itemオブジェクト生成のためのUserオブジェクトを生成する...post_user_obj
        Itemオブジェクトを生成する...item_obj1
        取引相手としてUserオブジェクトを生成する...participant
        DMオブジェクトに関連のないUserオブジェクトを作成する...acces_user_obj
        """
        category_obj = Category.objects.create(number="Donar o vender")
        post_user_obj = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        item_obj1 =  Item.objects.create(user=post_user_obj, id=1, title="テストアイテム１", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        participant = User.objects.create_user(username="participant", email="test_participant@gmail.com", password='12345')
        acces_user_obj = User.objects.create_user(username="access_user", email="test_access_user@gmail.com", password='12345')
    
    def test_should_redirect_HOME_for_anonymous_user(self):
        # 未認証ユーザーのアクセスの場合HOMEにリダイレクトする。*1

        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(str(item_obj.id),)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)
        
        self.client = Client()
        login_status = self.client.logout()
        self.assertFalse(login_status)
        dm_id = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.get(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=(str(dm_id),)), follow=True)
        templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.HOME in templates) # *1



    def test_should_redirect_HOME_for_authenticated_access_user(self):
        # アクセスユーザーがDirectMessageに関連しないユーザー(owner, participantではないユーザー)の場合HOMEにリダイレクトする。*2

        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(str(item_obj.id),)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)

        self.client = Client()
        login_status = self.client.login(username="access_user", password="12345")
        self.assertTrue(login_status)
        dm_id = Item.objects.get(id=item_obj.id).direct_message.id
        response = self.client.get(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=(str(dm_id),)), follow=True)
        templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.HOME in templates) # *2


    def test_should_create_dm_content_by_Participant(self):
        # endpoint送信後、formが適切であればDirectMassageContentが一つ生成される。*3

        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(str(item_obj.id),)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)
        before_create_dm_content_count = Item.objects.get(id=item_obj.id).direct_message.direct_message_contents.all().count()

        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status)
        dm_id = Item.objects.get(id=item_obj.id).direct_message.id
        data = {"content": "kvsavpovkv"}
        response = self.client.post(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=(str(dm_id),)), data, follow=True)
        #templates = [ele.name for ele in response.templates]
        #self.assertTrue(TemplateName.HOME in templates) # *2
        after_create_dm_content_count = Item.objects.get(id=item_obj.id).direct_message.direct_message_contents.all().count()
        self.assertEqual(after_create_dm_content_count, before_create_dm_content_count+1)


    def test_should_add_dm_content_to_dm(self):
        # endpoint送信後、formが適切であればDirectMassageContentがDirectMessageに加えられる。*4
        
        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(str(item_obj.id),)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)
        #before_create_dm_content_count = Item.objects.get(id=item_obj.id).direct_message.direct_message_contents.all().count()

        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status)
        dm_id = Item.objects.get(id=item_obj.id).direct_message.id
        data = {"content": "kvsavpovkv"}
        response = self.client.post(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=(str(dm_id),)), data, follow=True)

        dm_content_obj = DirectMessageContent.objects.get(content=data["content"])
        dm_content_objects = Item.objects.get(id=1).direct_message.direct_message_contents.all()
        self.assertTrue(dm_content_obj in dm_content_objects) #*4
        

    def test_should_redirect_to_ITEM_DETAIL(self):
        # endpoint送信後、formが適切であればDM詳細ページにリダイレクトされる*5

        #DMオブジェクトを作るところから始める
        item_obj = Item.objects.get(id=1)
        
        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        self.client.post(reverse_lazy(ViewName.SOLICITUD_INPUT, args=(str(item_obj.id),)), data={"message":"csdmfmvf"}, follow=True)
        #記事作成者が取引相手を定める(DirectMessageオブジェクト生成)
        self.client = Client()
        login_status = self.client.login(username="post_user", password="12345")
        self.assertTrue(login_status) #認証状態でアクセスを行う
        solicitud_id = Item.objects.get(id=item_obj.id).solicitudes.all().first().id
        data = {"id": solicitud_id}
        response = self.client.post(reverse_lazy(ViewName.SOLICITUD_SELECT, args=(str(solicitud_id),)), data, follow=True)
        #before_create_dm_content_count = Item.objects.get(id=item_obj.id).direct_message.direct_message_contents.all().count()

        self.client = Client()
        login_status = self.client.login(username="participant", password="12345")
        self.assertTrue(login_status)
        dm_id = Item.objects.get(id=item_obj.id).direct_message.id
        data = {"content": "kvsavpovkv"}
        response = self.client.post(reverse_lazy(ViewName.DIRECT_MESSAGE_DETAIL, args=(str(dm_id),)), data, follow=True)
        templates = [ele.name for ele in response.templates]
        self.assertTrue(TemplateName.DIRECT_MESSAGE_DETAIL in templates)








