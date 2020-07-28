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





class UsernameChangeViewGETTest(TestCase):
    """テスト目的
    ユーザーネームの編集ページにアクセスできることを担保する
    """
    """テスト対象
    config/views.py  UsernameChangeView
    endpont: "username_change/"
    name: "username_change"
    Get methodのみ
    """
    """テスト項目
    済 ユーザーがprofile編集ページにアクセスすることができる ...*1
    済 ユーザーネームをチェンジする逆引きurlを使ったらユーザーネームを変更するページが表示される ...*2
    表示されるプロフィール編集ページに逆引きurl<a href="/username_change/">が要素として含まれているか　...*3
    """

    def setUp(self):
        """テスト環境
        ユーザーを作成する
        """
        self.user_obj, self.profile_obj = create_user_for_test(create_user_data(prefix_user_emailaddress="test1"))
                
    def test_ユーザーがprofile編集ページつまりprofiles_profile_html_にアクセスすることができる(self):
        self.client = Client()
        login_status = self.client.login(username="test1", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセス
        #profile編集ページにアクセスする
        response = self.client.get(reverse_lazy(ViewName.PROFILE_EDIT), follow=True)
        self.assertEqual(response.status_code, 200)
        #print(get_templates_by_response(response))
        self.assertTrue('profiles/profile.html' in get_templates_by_response(response)) #*1

    def test_ユーザーネームをチェンジする逆引きurlを使ったらユーザーネームを変更するページが表示される(self):
        self.client = Client()
        login_status = self.client.login(username="test1", password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセス

        #ユーザーネーム編集ページにアクセスする EDIT_USERNAME
        response = self.client.get(reverse_lazy(ViewName.EDIT_USERNAME), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('config/change_username.html' in get_templates_by_response(response)) #*2

"""
    def test_表示されるプロフィール編集ページに逆引きurl_a_href_username_changeが要素として含まれているか(self):
        self.client = Client()
        login_status = self.client.login(username=self.user_obj.username, password='1234tweet')
        self.assertTrue(login_status) #認証状態でアクセス
        #profile編集ページにアクセスする
        response = self.client.get(reverse_lazy(ViewName.PROFILE_EDIT), follow=True)
        self.assertEqual(response.status_code, 200)
        #print(get_templates_by_response(response))
        #print(response)
        #print(type(response))
        #print(dir(response))
        print(response.context)
        #print(response.content)
        self.assertContains( response, "username", status_code=200) #*3
        self.assertTrue('profile_obj' in response.context)

"""

