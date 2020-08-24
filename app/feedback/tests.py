from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy
# Create your tests here.
from feedback.models import Feedback
from feedback.views import FeedbackView
from feedback.forms import FeedbackModelForm
from django.contrib import auth
from config.tests.utils import *
from config.constants import TemplateName, ViewName

from django.contrib.auth.models import User
from categories.models      import Category
from items.models           import Item
from direct_messages.models import DirectMessage
from favorite.models        import Favorite
from profiles.models        import Profile
from solicitudes.models     import Solicitud
import django



class ShowFeedbackFormViewTest(TestCase):
    """テスト目的


    """
    """テスト対象
    feedback.views.py ShowFeedbackFormView()
    """
    """テスト項目
    未認証ユーザーによるアクセスはhomeにリダイレクトされる*1

    """
    URL_FORMAT = "direct_messages/{}/"
    HOME_TEMPLATE = "config/home.html"

    def setUp(self):
        category_obj  = Category.objects.create(number="Donar o vender")
        post_user_obj = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        item_obj1     =  Item.objects.create(user=post_user_obj, id=1, title="テストアイテム１", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        post_user_profile_obj = Profile.objects.get(user=post_user_obj)
        participant   = User.objects.create_user(username="participant", email="test_participant@gmail.com", password='12345')
        participant_profile_obj = Profile.objects.get(user=participant)
        dm_obj = DirectMessage.objects.create(id=2, item=item_obj1, owner=post_user_profile_obj, participant=participant_profile_obj)


    def test_should_riderct_for_anonymous_user(self):
        #未認証ユーザーによるアクセスはhomeにリダイレクトされる*1
        self.client = Client()
        self.client.logout()
        dm_obj = DirectMessage.objects.get(id=2)
        url = self.URL_FORMAT.format(str(dm_obj.id))
        print(url)
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        templates = [ele.name for ele in response.templates]
        self.assertTrue(self.HOME_TEMPLATE)







class FeedbackViewTest(TestCase):
    """テスト目的
    フィードバックデータの入力を受け取り、関連するオブジェクトの生成や変更が適切に実行されることを担保する

    DirectMessage.is_feedbacked_by_participantの変更
    DirectMessage.is_feedbacked_by_ownerの変更
    Feedbackオブジェクトの生成
    Profile.feedbackにFeedbackオブジェクトの追加

    """
    """テスト対象
    feedback.views.py FeedbackViewTest()
    endpoit: "feedback/feedback/"
    name: "feedback:feedback" 
    """
    """テスト項目
    FeedbackModelFormのcontentが入力されていないときは?
    未認証ユーザーがpostアクセスした場合にはhomeにリダイレクトされる。(homeのテンプレート"config/home.html"が使われる) *1
    ユーザーがDirectMessageオブジェクトの主または参加者どちらでもない場合にはhomeにリダイレクトされる。*2
    入力されたフォームデータが不適切な場合には、feedback生成ページがリダイレクトされる。(テンプレートは'feedback/show_feedback_form.html') *3
    入力されたフォームデータが適切な場合には、アイテム詳細ページにリダイレクトされる。(テンプレートはTemplateKey.ITEM_DETAILが使われる)*4
    入力されたフォームデータが適切な場合にはFeedbackオブジェクトが生成される。*5
    アイテム記事の主がフィードバックを入力し、データが適切な場合には、dm_obj.is_feedbacked_by_ownerの値がTrueに変更される(前後チェック)*6
    アイテム記事の主がフィードバックを入力し、データが適切な場合には、アイテム記事参加者のProfile.feedbackにFeedbackオブジェクトが追加される。*7
    アイテム記事参加者がフィードバックを入力し、データが適切な場合には、dm_obj.is_feedbacked_by_participantの値がTrueに変更される(前後チェック)*8
    アイテム記事参加者がフィードバックを入力し、データが適切な場合には、アイテム記事主のProfile.feedbackにFeedbackオブジェクトが追加される。*9

    """
    url = 'feedback/'

    def setUp(self):
        """テスト環境
        互いに独立するテストを実行するためsetUpは今回使わない
        """

    
    def test_未認証ユーザーがpostアクセスした場合にはhomeにリダイレクトされる(self):
        category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_user_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))
        item_obj1 = create_item_for_test(post_user_obj, create_item_data(category_obj))
        participant, participant_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="participant"))
        solicitud_obj = create_solicitud_for_test(item_obj1, participant, create_solicitud_data(message=None))
        dm_obj, item_obj1 = create_direct_message_for_test(solicitud_obj)

        self.client = Client()
        login_status = self.client.logout()
        session = self.client.session
        session['dm_obj_pk'] = dm_obj.id
        session.save()
        self.assertFalse(login_status) #未認証状態でアクセス
        user = auth.get_user(self.client)
        self.assertEqual(type(user), django.contrib.auth.models.AnonymousUser) # userがAnonymousUserであることを担保
        valid_form_data = {"content":"良かった", "level":2}
        valid_form_data["evaluator"] = user
        url = reverse_lazy(ViewName.FEEDBACK_POST)
        response = self.client.post(url, valid_form_data, follow=True)
        self.assertTrue(response.status_code, 200)
        templates = [ template.name for template in response.templates ] 
        self.assertTrue(TemplateName.HOME in templates) #未認証ユーザーがpostアクセスした場合にはhomeにリダイレクトされる


    def test_ユーザーがDirectMessageオブジェクトの主または参加者どちらでもない場合にはhomeにリダイレクトされる(self):  
        category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_user_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))
        item_obj1 = create_item_for_test(post_user_obj, create_item_data(category_obj))
        participant, participant_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="participant"))
        solicitud_obj = create_solicitud_for_test(item_obj1, participant, create_solicitud_data(message=None))
        dm_obj, item_obj1 = create_direct_message_for_test(solicitud_obj)
     
        #新規ユーザー作成
        new_user_obj, new_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="new_user"))
        self.client = Client()
        login_status = self.client.login(username=new_user_obj.username, password="1234tweet")
        self.assertTrue(login_status) #認証状態でアクセス
        session = self.client.session
        session['dm_obj_pk'] = dm_obj.id
        session.save()
        post_user = User.objects.get(username="post_user")
        valid_form_data = {"content":"良かった", "level":2}
        valid_form_data["evaluator"] = post_user
        url = reverse_lazy(ViewName.FEEDBACK_POST)
        response = self.client.post(url, valid_form_data, follow=True)
        self.assertTrue(response.status_code, 200)
        templates = [ template.name for template in response.templates ]
        self.assertTrue(TemplateName.HOME in templates) #ユーザーがDirectMessageオブジェクトの主または参加者どちらでもない場合にはhomeにリダイレクトされる    
    


    def test_入力されたフォームデータが適切な場合にはアイテム詳細ページにリダイレクトされる(self):
        category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_user_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))
        item_obj1 = create_item_for_test(post_user_obj, create_item_data(category_obj))
        participant, participant_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="participant"))
        solicitud_obj = create_solicitud_for_test(item_obj1, participant, create_solicitud_data(message=None))
        dm_obj, item_obj1 = create_direct_message_for_test(solicitud_obj)  

        # post_userがアクセスする
        self.client = Client()
        login_status = self.client.login(username="post_user", password="1234tweet")
        self.assertTrue(login_status) #認証状態でアクセス
        session = self.client.session
        session['dm_obj_pk'] = dm_obj.id
        session.save()

        
        valid_form_data = {"content":"良かった", "level":2}
        valid_form_data["evaluator"] = post_user_obj
        form = FeedbackModelForm(valid_form_data)
        self.assertTrue(form.is_valid())

        url = reverse_lazy(ViewName.FEEDBACK_POST)
        response = self.client.post(url, valid_form_data, follow=True)
        self.assertTrue(response.status_code, 200)
        templates = [ template.name for template in response.templates ]
        self.assertTrue(TemplateName.ITEM_DETAIL in templates)


    def test_入力されたフォームデータが適切な場合にはFeedbackオブジェクトが生成される(self):
        category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_user_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))
        item_obj1 = create_item_for_test(post_user_obj, create_item_data(category_obj))
        participant, participant_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="participant"))
        solicitud_obj = create_solicitud_for_test(item_obj1, participant, create_solicitud_data(message=None))
        dm_obj, item_obj1 = create_direct_message_for_test(solicitud_obj)


        #テスト開始段階のFeedbackのオブジェクト数
        feedback_objects_count = Feedback.objects.all().count()
        self.assertEqual(feedback_objects_count, 0)

        # post_userがアクセスする
        self.client = Client()
        login_status = self.client.login(username="post_user", password="1234tweet")
        self.assertTrue(login_status) #認証状態でアクセス
        session = self.client.session
        session['dm_obj_pk'] = dm_obj.id
        session.save()

        
        valid_form_data = {"content":"良かった", "level":2}
        valid_form_data["evaluator"] = post_user_obj
        form = FeedbackModelForm(valid_form_data)
        self.assertTrue(form.is_valid())

        url = reverse_lazy(ViewName.FEEDBACK_POST)
        response = self.client.post(url, valid_form_data, follow=True)
        self.assertTrue(response.status_code, 200)
        templates = [ template.name for template in response.templates ]
        self.assertTrue(TemplateName.ITEM_DETAIL in templates)

        after_feedback_objects_count = Feedback.objects.all().count()
        self.assertEqual(after_feedback_objects_count, feedback_objects_count+1)


    def test_アイテム記事の主がフィードバックを入力しデータが適切な場合には_dm_obj_is_feedbacked_by_ownerの値がTrueに変更される(self):
        category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_user_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))
        item_obj1 = create_item_for_test(post_user_obj, create_item_data(category_obj))
        participant, participant_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="participant"))
        solicitud_obj = create_solicitud_for_test(item_obj1, participant, create_solicitud_data(message=None))
        dm_obj, item_obj1 = create_direct_message_for_test(solicitud_obj)

        self.assertFalse(dm_obj.is_feedbacked_by_owner)
        # post_userがアクセスする
        self.client = Client()
        login_status = self.client.login(username="post_user", password="1234tweet")
        self.assertTrue(login_status) #認証状態でアクセス
        session = self.client.session
        session['dm_obj_pk'] = dm_obj.id
        session.save()

        #適切なデータを作成
        valid_form_data = {"content":"良かった", "level":2}
        valid_form_data["evaluator"] = post_user_obj
        form = FeedbackModelForm(valid_form_data)
        self.assertTrue(form.is_valid())

        #is_feedbacked_by_ownerの値が変更されたかチェックする
        url = reverse_lazy(ViewName.FEEDBACK_POST)
        response = self.client.post(url, valid_form_data, follow=True)
        self.assertTrue(response.status_code, 200)
        new_dm_obj = DirectMessage.objects.get(id=dm_obj.id)
        self.assertTrue(new_dm_obj.is_feedbacked_by_owner)

        #is_feedbacked_by_participantの値が変更されないままかチェックする
        self.assertFalse(new_dm_obj.is_feedbacked_by_participant)


    def test_アイテム記事の主がフィードバックを入力しデータが適切な場合にはアイテム記事参加者のProfile_feedbackにFeedbackオブジェクトが追加される(self):
        category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_user_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))
        item_obj1 = create_item_for_test(post_user_obj, create_item_data(category_obj))
        participant, participant_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="participant"))
        solicitud_obj = create_solicitud_for_test(item_obj1, participant, create_solicitud_data(message=None))
        dm_obj, item_obj1 = create_direct_message_for_test(solicitud_obj)

        #self.assertFalse(self.dm_obj.is_feedbacked_by_owner)
        feedback_count = post_user_profile_obj.feedback.all().count()
        self.assertEqual(feedback_count, 0)
        # post_userがアクセスする
        self.client = Client()
        login_status = self.client.login(username="post_user", password="1234tweet")
        self.assertTrue(login_status) #認証状態でアクセス
        session = self.client.session
        session['dm_obj_pk'] = dm_obj.id
        session.save()

        #適切なデータを作成
        valid_form_data = {"content":"良かった", "level":2}
        valid_form_data["evaluator"] = post_user_obj
        form = FeedbackModelForm(valid_form_data)
        self.assertTrue(form.is_valid())

        # 記事主が参加者に対しフィードバックを残す
        url = reverse_lazy(ViewName.FEEDBACK_POST)
        response = self.client.post(url, valid_form_data, follow=True)
        self.assertTrue(response.status_code, 200)
        new_dm_obj = DirectMessage.objects.get(id=dm_obj.id)
        self.assertTrue(new_dm_obj.is_feedbacked_by_owner)
        # 記事参加者のProfile_feedbackにFeedbackオブジェクトが追加されるかチェックする
        new_count = Profile.objects.get(user=participant).feedback.all().count()
        self.assertEqual(new_count, feedback_count+1)


    def test_アイテム記事参加者がフィードバックを入力しデータが適切な場合にはdm_obj_is_feedbacked_by_participantの値がTrueに変更される(self):
        category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_user_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))
        item_obj1 = create_item_for_test(post_user_obj, create_item_data(category_obj))
        participant, participant_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="participant"))
        solicitud_obj = create_solicitud_for_test(item_obj1, participant, create_solicitud_data(message=None))
        dm_obj, item_obj1 = create_direct_message_for_test(solicitud_obj)

        #初期の状態ではis_feedbacked_by_participantはFalseであることを確認する
        self.assertFalse(dm_obj.is_feedbacked_by_participant)
        # post_userがアクセスする
        self.client = Client()
        login_status = self.client.login(username="participant", password="1234tweet")
        self.assertTrue(login_status) #認証状態でアクセス
        session = self.client.session
        session['dm_obj_pk'] = dm_obj.id
        session.save()

        #適切なデータを作成
        valid_form_data = {"content":"良かった", "level":2}
        valid_form_data["evaluator"] = participant
        form = FeedbackModelForm(valid_form_data)
        self.assertTrue(form.is_valid())

        #is_feedbacked_by_participantの値が変更されたかチェックする
        url = reverse_lazy(ViewName.FEEDBACK_POST)
        response = self.client.post(url, valid_form_data, follow=True)
        self.assertTrue(response.status_code, 200)
        new_dm_obj = DirectMessage.objects.get(id=dm_obj.id)
        self.assertTrue(new_dm_obj.is_feedbacked_by_participant)

        #is_feedbacked_by_ownerの値が変更されないままかチェックする
        self.assertFalse(new_dm_obj.is_feedbacked_by_owner) 


    def test_アイテム記事参加者がフィードバックを入力しデータが適切な場合にはアイテム記事主のProfile_feedbackにFeedbackオブジェクトが追加される(self): 
        category_obj = pickUp_category_obj_for_test()
        post_user_obj, post_user_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="post_user"))
        item_obj1 = create_item_for_test(post_user_obj, create_item_data(category_obj))
        participant, participant_profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="participant"))
        solicitud_obj = create_solicitud_for_test(item_obj1, participant, create_solicitud_data(message=None))
        dm_obj, item_obj1 = create_direct_message_for_test(solicitud_obj)

        #self.assertFalse(self.dm_obj.is_feedbacked_by_owner)
        feedback_count = post_user_profile_obj.feedback.all().count()
        self.assertEqual(feedback_count, 0)
        # post_userがアクセスする
        self.client = Client()
        login_status = self.client.login(username="participant", password="1234tweet")
        self.assertTrue(login_status) #認証状態でアクセス
        session = self.client.session
        session['dm_obj_pk'] = dm_obj.id
        session.save()

        #適切なデータを作成
        valid_form_data = {"content":"良かった", "level":2}
        valid_form_data["evaluator"] = participant
        form = FeedbackModelForm(valid_form_data)
        self.assertTrue(form.is_valid())

        # 参加者が記事主に対しフィードバックを残す
        url = reverse_lazy(ViewName.FEEDBACK_POST)
        response = self.client.post(url, valid_form_data, follow=True)
        self.assertTrue(response.status_code, 200)
        new_dm_obj = DirectMessage.objects.get(id=dm_obj.id)
        # 参加者によるフィードバックがTrueに切り替えられるか確認
        self.assertTrue(new_dm_obj.is_feedbacked_by_participant)

        # 記事主のProfile_feedbackにFeedbackオブジェクトが追加されるかチェックする
        new_count = Profile.objects.get(user=post_user_obj).feedback.all().count()
        self.assertEqual(new_count, feedback_count+1)
       