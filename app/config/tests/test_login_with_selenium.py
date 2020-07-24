from django.test import LiveServerTestCase, Client
from django.urls import reverse_lazy
#from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from django.contrib.auth.models import User
from time import sleep
from allauth.account.models import EmailAddress
"""


#　テスト実行方法
# python manage.py test config.tests.test_login

#seleniumを使ったテストではまず最初にサーバーを起動しておくことが前提である。これができてないとエラーが出る
#またサーバーを起動してもurlやポート違いでエラーが出ることがあるので確認すること
#https://stackoverflow.com/questions/32828943/django-selenium-fails-to-load-localhost



#メモ
#User.objects.create_user()ではその後認証する事ができなかった。seleniumでユーザー作成することが必要だと判明した。

BASE_URL = "http://127.0.0.1:8000"





class LogInTestCase(LiveServerTestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920,1080') 
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        #self.driver.implicitly_wait(5)
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())



        #user_obj = User.objects.create_user(username="chiaki", password="tweet1234", email="chiaki@mail.com")
        #EmailAddress.objects.create(user=user_obj, email="chiaki@mail.com")
        data = {"email":"chiaki@mail.com", "password":"1234tweet"}
        url = BASE_URL + "/accounts/signup/"
        self.driver.get(url)
        email_form = self.driver.find_element_by_id("id_email")
        email_form.send_keys("chiaki@mail.com")

        password_form1 = self.driver.find_element_by_id("id_password1")
        password_form1.send_keys("1234tweet")

        
        password_form2 = self.driver.find_element_by_id("id_password2")
        password_form2.send_keys("1234tweet")

        btn = self.driver.find_element_by_id("signup_form").find_element_by_tag_name("button")
        btn.click()


        



    def tearDown(self):
        self.driver.quit()


    def test_ベーシック認証でログインを実行し認証する(self):

        url = BASE_URL + str(reverse_lazy("account_login"))
        #print(url)

        self.driver.get(url)

        mail_form = self.driver.find_element_by_id("id_login")
        input_data_mail = "chiaki@mail.com"
        mail_form.send_keys(input_data_mail)


        password_form = self.driver.find_element_by_id("id_password")
        input_data_password = "1234tweet"
        password_form.send_keys(input_data_password)
        sleep(3)

        login_btn = self.driver.find_element_by_id("btn_sign_in")
        #login_btn = self.driver.find_element_by_class_name("primaryAction.btn.btn-block.btn-primary")
        login_btn.click()
        sleep(3)

        #print(self.driver.current_url)
        self.assertEqual(self.driver.current_url, BASE_URL+str(reverse_lazy("home")))


    def test_ベーシック認証でログインを実行し誤ったパスワードで認証失敗する(self):

        url = BASE_URL + str(reverse_lazy("account_login"))
        #print(url)

        self.driver.get(url)

        mail_form = self.driver.find_element_by_id("id_login")
        input_data_mail = "chiaki@mail.com"
        mail_form.send_keys(input_data_mail)

        sleep(3)


        password_form = self.driver.find_element_by_id("id_password")
        input_data_password = "12"
        password_form.send_keys(input_data_password)

        login_btn = self.driver.find_element_by_class_name("primaryAction.btn.btn-block.btn-primary")
        login_btn.click()

        sleep(3)

        #print(self.driver.current_url)
        self.assertEqual(self.driver.current_url, BASE_URL + str(reverse_lazy("account_login")))        



"""



