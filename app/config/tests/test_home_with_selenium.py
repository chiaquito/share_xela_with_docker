from django.test import LiveServerTestCase
from django.urls import reverse_lazy
#from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from django.contrib.auth.models import User
from config.constants import ViewName

"""

#　テスト実行方法
# python manage.py test config.tests

#seleniumを使ったテストではまず最初にサーバーを起動しておくことが前提である。これができてないとエラーが出る
#またサーバーを起動してもurlやポート違いでエラーが出ることがあるので確認すること
#https://stackoverflow.com/questions/32828943/django-selenium-fails-to-load-localhost


BASE_URL = "http://127.0.0.1:8000"





class HomeTestCase(LiveServerTestCase):


    
    def setUp(self):

        #PROXY = "127.0.0.1:8000" # IP:PORT or HOST:PORT
        PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT

        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--proxy-server=%s' % PROXY)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920,1080') 
        #self.driver.Chrome(options=chrome_options)

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
        #self.driver = webdriver.Safari()
        User.objects.create_user(username="chiaki", password="12345", email="chiaki@mail.com")



    def tearDown(self):
        self.driver.quit()



    def test_ホームのタイトルとメニューのリンク先が正しいかチェックする(self):
        url = BASE_URL + str(reverse_lazy("home"))
        self.driver.get(url)
        print(self.driver)
        print(self.driver.current_url)
        #print(self.driver.page_source)
        #Gente de Guatemalaが表示されていなければならない
        title_guatemala = self.driver.find_element_by_id("title_guatemala")
        text_title_guatemala = title_guatemala.text
        self.assertTrue("Gente de Guatemala" in text_title_guatemala)

        #Gente de Tu departamentoが表示されていなければならない
        title_local = self.driver.find_element_by_id("title_local")
        text_title_local = title_local.text
        self.assertTrue("Gente de Tu departamento" in text_title_local)



        menu_guatemala = self.driver.find_element_by_id("menu_guatemala")
        menu_group = menu_guatemala.find_elements_by_tag_name("h5")

        for num in range(len(menu_group)):
            title = menu_group[num].find_element_by_tag_name("a").text
            if num == 0:
                self.assertTrue("quiere donar o vender" in title)
            elif num == 1:
                self.assertTrue("busca donante" in title)                
            elif num == 2:
                self.assertTrue("quiere avisar" in title)
            elif num == 3:
                self.assertTrue("busca una habitación" in title)
            elif num == 4:
                self.assertTrue("alquila una habitación" in title)
            elif num == 5:
                self.assertTrue("busca pensionado" in title)
            elif num == 6:
                self.assertTrue("busca pensionista" in title)
            elif num == 7:
                self.assertTrue("busca empleado" in title)
            elif num == 8:
                self.assertTrue("busca trabajador" in title)
            elif num == 9:
                self.assertTrue("publicidad de Enpresas y Servicios" in title)
            
            href = menu_group[num].find_element_by_tag_name("a").get_attribute('href')
            self.assertEqual(href, BASE_URL + str(reverse_lazy("items:ItemCategoryListView", args=(str(num+1),))))





        menu_local = self.driver.find_element_by_id("menu_local")
        menu_group = menu_local.find_elements_by_tag_name("h5")

        for num in range(len(menu_group)):
            title = menu_group[num].find_element_by_tag_name("a").text
            if num == 0:
                self.assertTrue("quiere donar o vender" in title)
            elif num == 1:
                self.assertTrue("busca donante" in title)                
            elif num == 2:
                self.assertTrue("quiere avisar" in title)
            elif num == 3:
                self.assertTrue("busca una habitación" in title)
            elif num == 4:
                self.assertTrue("alquila una habitación" in title)
            elif num == 5:
                self.assertTrue("busca pensionado" in title)
            elif num == 6:
                self.assertTrue("busca pensionista" in title)
            elif num == 7:
                self.assertTrue("busca empleado" in title)
            elif num == 8:
                self.assertTrue("busca trabajador" in title)
            elif num == 9:
                self.assertTrue("publicidad de Enpresas y Servicios" in title)
            
            href = menu_group[num].find_element_by_tag_name("a").get_attribute('href')
            self.assertEqual(href, BASE_URL + str(reverse_lazy("items:ItemCategoryLocalListView", args=(str(num+1),))))





    def test_ShareXelaをクリックするとHome画面に遷移する(self):
        url = BASE_URL + str(reverse_lazy("home"))
        self.driver.get(url) 
        
        bavbar_brand = self.driver.find_element_by_class_name("navbar-brand")
        self.assertTrue("ShareXela" in bavbar_brand.text)

        href = bavbar_brand.get_attribute("href")
        self.assertEqual(href, BASE_URL + str(reverse_lazy("home")))

        before_html = self.driver.page_source
        bavbar_brand.click()
        after_html = self.driver.page_source
        self.assertEqual(before_html, after_html)



    def test_未認証状態でアクセスした場合にNavbarのメニューの画面遷移先が正しい(self):
        url = BASE_URL + str(reverse_lazy("home"))
        self.driver.get(url) 

        navbar_menu = self.driver.find_element_by_id("navbar_menu").find_elements_by_tag_name("li")
        for num in range(len(navbar_menu)):
            if num == 0:
                nav_text = navbar_menu[num].find_element_by_tag_name("a").text
                self.assertTrue("Articulos" in  nav_text)
                href = navbar_menu[num].find_element_by_tag_name("a").get_attribute("href")
                self.assertEqual(href, BASE_URL+str(reverse_lazy("home")))

            elif num == 1:
                nav_text = navbar_menu[num].find_element_by_tag_name("a").text
                self.assertTrue("Avisos" in  nav_text)
                href = navbar_menu[num].find_element_by_tag_name("a").get_attribute("href")
                self.assertEqual(href, BASE_URL+str(reverse_lazy("avisos:avisos_alllist")))

            elif num == 2:
                nav_text = navbar_menu[num].find_element_by_tag_name("a").text
                self.assertTrue("Mi pagina" in  nav_text)
                
                #dropdownメニューは次のテストで実行する

            elif num == 3:
                nav_text = navbar_menu[num].find_element_by_tag_name("a").text
                self.assertTrue("Como usar" in  nav_text)
                href = navbar_menu[num].find_element_by_tag_name("a").get_attribute("href")
                self.assertEqual(href, BASE_URL+str(reverse_lazy("howto")))

            elif num == 4:
                nav_text = navbar_menu[num].find_element_by_tag_name("a").text
                self.assertTrue("Iniciar sesión" in  nav_text)
                href = navbar_menu[num].find_element_by_tag_name("a").get_attribute("href")
                self.assertEqual(href, BASE_URL+str(reverse_lazy("account_login")))            




    def test_未認証状態でアクセスした場合にdropdown_menuのメニューの画面遷移先が正しい(self):
        url = BASE_URL + str(reverse_lazy("home"))
        self.driver.get(url) 

        dropdown_menu = self.driver.find_element_by_id("navbarDropdown").click()
        dropdown_menu = self.driver.find_element_by_id("dropdown-menu").find_elements_by_tag_name("a")


        for num in range(len(dropdown_menu)):
            if num == 0:
                nav_text = dropdown_menu[num].text
                print(nav_text)
                self.assertTrue("Mis articulos" in  nav_text)
                href = dropdown_menu[num].get_attribute("href")
                self.assertEqual(href, BASE_URL+str(reverse_lazy("mypages:item_mylist")))

            elif num == 1:
                nav_text = dropdown_menu[num].text
                self.assertTrue("Crear articulo" in  nav_text)
                href = dropdown_menu[num].get_attribute("href")
                self.assertEqual(href, BASE_URL+str(reverse_lazy(ViewName.ITEM_CREATE)))

            elif num == 2:
                nav_text = dropdown_menu[num].text
                self.assertTrue("Editar Prefil" in  nav_text)
                href = dropdown_menu[num].get_attribute("href")
                self.assertEqual(href, BASE_URL+str(reverse_lazy("profiles:profile")))                
                

            elif num == 3:
                nav_text = dropdown_menu[num].text
                self.assertTrue("Articulos favoritos" in  nav_text)
                href = dropdown_menu[num].get_attribute("href")
                self.assertEqual(href, BASE_URL+str(reverse_lazy("items:item_list_by_favorite")))






"""