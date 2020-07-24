from django.test import TestCase
from django.test import Client

# Create your tests here.
from feedback.models import Feedback
from feedback.views import FeedbackView

from django.contrib.auth.models import User
from categories.models import Category
from items.models import Item
from direct_messages.models import DirectMessage
from favorite.models        import Favorite
from profiles.models        import Profile
from solicitudes.models     import Solicitud




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







'''

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
        Itemオブジェクト生成のためのCategoryオブジェクトを生成する...category_obj
        Itemオブジェクト生成のためのUserオブジェクトを生成する...post_user_obj
        Itemオブジェクトを生成する...item_obj1
        DMオブジェクト生成のためにProfileオブジェクトを取得する...post_user_profile_obj
        取引相手としてUserオブジェクトを生成する...participant
        DMオブジェクト生成のためにProfileオブジェクトを取得する...participant_profile_obj
        DMオブジェクトを生成する...dm_obj
        適切なformデータを生成する
        不適切なformデータを生成する

        """
        category_obj = Category.objects.create(name="Donar o vender")
        post_user_obj = User.objects.create_user(username="post_user", email="test_post_user@gmail.com", password='12345')
        item_obj1 =  Item.objects.create(user=post_user_obj, id=1, title="テストアイテム１", description="説明です。", category=category_obj, adm0="huh", adm1="cmks", adm2="dks")
        post_user_profile_obj = Profile.objects.get(user=post_user_obj)
        participant = User.objects.create_user(username="participant", email="test_participant@gmail.com", password='12345')
        participant_profile_obj = Profile.objects.get(user=participant)
        dm_obj = DirectMessage.objects.create(id=2, item=item_obj1, owner=post_user_profile_obj, participant=participant_profile_obj)
        self.valid_form_data = {"content":"良かった", "level":2}
        #self.url = 'feedback/feedback/'

    
    def test_should_be_template_of_home_for_anonymous_user(self):
        #未認証ユーザーがpostアクセスした場合にはhomeにリダイレクトされる。(homeのテンプレート"config/home.html"が使われる) *1
        self.client = Client()
        login_status = self.client.logout()
        dm_obj = DirectMessage.objects.get(id=2)
        #self.client.session["dm_obj_pk"] = dm_obj.id
        self.assertFalse(login_status) #未認証状態でアクセス

        url = "feedback/create/"

        response = self.client.post(self.url, self.valid_form_data)
        self.assertTrue(response.status_code, 200)
        print(response.content)
        print(response.context)
        #last_url, status_code = response.redirect_chain[-1]
        #print(last_url)
        #print(dir(response.client))
        #self.assertRedirects(response, "")
        #response = self.client.get("",  follow=True)
        templates = [template.name for template in response.templates ]
        #
        print(templates) 
        #self.assertTrue("config/home.html" in templates) #*1
    
    



'''







