# coding: utf-8

from django.test import TestCase
from django.test import Client

from django.contrib.auth.models import User
from solicitudes.models import Solicitud
from profiles.models import Profile
from items.models import Item
from items.forms  import ItemModelForm
from django.urls import reverse, reverse_lazy

from config.constants import ViewName
from config.forms import MyCustomSignupForm
from categories.models import CATEGORY_CHOICE, Category
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

import json



class TestConstants(object):
    DEFAULT_PASSWOD = "1234tweet"


def get_templates_by_response(response):
    templates = [ele.name for ele in response.templates]
    return templates



def setUp_cetegory_for_test():
    """機能
    categoryオブジェクトを生成する

    Args:
        -
    Returns:
        -
    """

    for ele in CATEGORY_CHOICE:
        value = ele[0]
        if Category.objects.filter(number=value).exists() != True:
            Category.objects.create(number=value)




def pickUp_category_obj_for_test():
    """使用例
    category_obj = pickUp_category_obj_for_test()

    """
    if Category.objects.exists():
        return Category.objects.all().last()
    else:
        setUp_cetegory_for_test()
        return Category.objects.all().last()




def create_user_data(prefix_user_emailaddress, password1=None, password2=None):
    """機能

    高階関数の引数として使うことを予定している

    Args:
        prefix_user_emailaddress:str 
        password1:str
        password2:str

    Returns:
        user_data:dict 例{"email":"post_user@gmail.com", "password1":"1234tweet", "password2": "1234tweet"}
    """

    data = {}
    email = prefix_user_emailaddress + "@gmail.com"
    data['email'] = email

    if password1 != None:
        data["password1"] = password1
    else:
        data["password1"] = TestConstants.DEFAULT_PASSWOD #"1234tweet"

    if password2 != None:
        data["password2"] = password2
    else:
        data["password2"] = TestConstants.DEFAULT_PASSWOD #"1234tweet"

    return data



#data = {"email":"postuser@gmail.com", "password1":"12345", "password2":"12345"}
def create_user_for_test(userData):
    """機能
    ユーザー登録を入力として生成したUserオブジェクト,Profileオブジェクトを返す
    返り値としては返さないが、ユーザー登録するAPIを叩くとUserオブジェクト、Profileオブジェクト、EmailAddressオブジェクトが生成される仕様である

    Args:
        userData:dict ...ユーザー作成用のデータ ex. userData = {"email":"postuser@gmail.com", "password1":"12345", "password2":"12345"}
    Returns:
        user_obj: Userオブジェクト
        profile_obj: Ptofileオブジェクト
    """

    CREATE_USER_URL = reverse(ViewName.SIGN_UP)
    client = Client()
    response = client.post(CREATE_USER_URL, userData)
    user_obj = User.objects.get(email=userData["email"])
    profile_obj = Profile.objects.get(user=user_obj)
    #userオブジェクトを生成するとEmailAddressオブジェクトも生成される仕様である
    # email_obj = EmailAddress.objects.get(email=userData["email"])
    return user_obj, profile_obj









def create_item_data(category_obj, title=None, price=None, description=None, adm0=None, adm1=None, adm2=None ):
    """機能

    高階関数の引数として使うことを予定している
    category_objの引数としてpickUp_category_obj_for_testを使うことができる

    変数countはItemオブジェクトをobjects.getする際にtitleを使って取得するが、単一の値を担保するために使う。
    """

    data = {}
    count = str(Item.objects.all().count())


    data['category'] = category_obj.id
    if title != None:
        data["title"] = title
    else:
        data["title"] = "テストアイテム" + count
    if price != None and type(price) == int:
        data["price"] = price
    else:
        data["price"] = 900

    if description != None:
        data["description"] = description
    else:
        data["description"] = "テストアイテム1の説明"

    if adm0 != None:
        data["adm0"] = adm0
    else:
        data["adm0"] = "GUATEMALA"

    if adm1 != None:
        data["adm1"] = adm1
    else:
        data["adm1"] = "Quetzaltenango"

    if adm2 != None:
        data["adm2"] = adm2
    else:
        data["adm2"] = "Quetzaltenango"

    #フォームのチェック
    form = ItemModelForm(data)
    if form.is_valid() == False:
        for ele in form.errors:
            print(ele)


    return data





def create_item_for_test(user_obj, item_data):
    """機能

    Args:
        user_obj: User ... 
        item_data:dict ... create_item_data()を引数として使える。

    Returns:
        item_obj: Item
    """

    CREATE_ITEM_URL = reverse(ViewName.ITEM_CREATE)
    client = Client()
    login_status = client.login(username=user_obj.username, password="1234tweet")
    #login_status = client.force_authenticate(user=user_obj)
    print("login_status :", login_status)
    response = client.post(CREATE_ITEM_URL, item_data)
    item_obj = Item.objects.get(title=item_data["title"])
    return item_obj






def create_solicitud_data(message=None):

    data = {}
    if message != None:
        data["message"] = message
    else:
        data["message"] = "申請内容"
    return data



def create_solicitud_for_test(item_obj, access_user_obj, solicitud_data):

    #access_userが申請する
    POST_SOLICITUD_URL = reverse(ViewName.SOLICITUD_INPUT, args=(item_obj.id,))
    client = Client()
    login_status = client.login(username=access_user_obj.username, password="1234tweet")
    client.post(POST_SOLICITUD_URL, solicitud_data)
    solicitud_obj = Solicitud.objects.all().last()
    return solicitud_obj



def create_direct_message_for_test(solicitud_obj):

    #SOLICITUD_SELECT
    SOLICITUD_SELECT_URL = reverse(ViewName.SOLICITUD_SELECT, args=(solicitud_obj.id,),)
    item_obj = Item.objects.get(solicitudes__id=solicitud_obj.id)
    post_user_obj = item_obj.user
    client = Client()
    login_status = client.login(username=post_user_obj.username, password="1234tweet")
    client.post(SOLICITUD_SELECT_URL)
    item_obj = Item.objects.get(solicitudes__id=solicitud_obj.id)
    dm_obj = item_obj.direct_message

    return dm_obj











"""
apiによるデータの取得ができるか。
webからケータイに移行した場合にはtokenが存在しないことにならないか?いや存在するか多分rest-authがtokenを返してくれるので大丈夫
"""



def create_user_for_android_test(userName):
    """使用例
    post_user_key = create_user_for_android_test("post_user")
    """
    """機能
    Userを登録する。
    
    (補足)User登録するだけでProfileオブジェクト、Tokenオブジェクト、EmailAddressオブジェクトが自動的に作成される

    Args:
        userName:str ...これからemailaddressを作成する元のusername

    Returns:
        key:str 
    """
    #https://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html#registration
    CREATE_USER_API_URL = reverse('rest_register')
    client = APIClient()


    email = userName + "@gmail.com"
    data = {"email": email, "password1":"1234tweet", "password2":"1234tweet"}

    response = client.post(CREATE_USER_API_URL, data)
    key = response.data["key"]
    return key






def create_item_data_for_android_test(
        category_obj, title=None, price=None, description=None,
        adm0=None, adm1=None, adm2=None, point=None, radius=None,
        ):
    """機能

    高階関数の引数として使うことを予定している
    category_objの引数としてpickUp_category_obj_for_testを使うことができる

    変数countはItemオブジェクトをobjects.getする際にtitleを使って取得するが、単一の値を担保するために使う。

    androidが送信するデータはCategoryオブジェクトでnumber属性は分かっているがidが不明のデータである。
    したがってそのようなデータを作成しなければならない。
    webappの場合はFormがカテゴリーオブジェクトを受け取る。
    これ違う。。。ModelFormの仕様上、category_objを利用してItemオブジェクト生成する場合には、category_obj.id値を渡さなければならない。

    androidappの場合にはcategoy_objがjson形式に変換されている。したがってcategory_objはjson形式に変更する。またid値は削除する。
    """

    item_data = {}
    count = str(Item.objects.all().count())


    item_data['category'] = { "number": category_obj.number }

    if title != None:
        item_data["title"] = title
    else:
        item_data["title"] = "テストアイテム" + count
    if price != None and type(price) == int:
        item_data["price"] = price
    else:
        item_data["price"] = 900

    if description != None:
        item_data["description"] = description
    else:
        item_data["description"] = "テストアイテム1の説明"

    if adm0 != None:
        item_data["adm0"] = adm0
    else:
        item_data["adm0"] = "GUATEMALA"

    if adm1 != None:
        item_data["adm1"] = adm1
    else:
        item_data["adm1"] = "Quetzaltenango"

    if adm2 != None:
        item_data["adm2"] = adm2
    else:
        item_data["adm2"] = "Quetzaltenango"

    if point != None:
        item_data["point"] = point 
    else:
        item_data["point"] = "SRID=4326;POINT (-91.5910384 14.8390624)"

    if radius != None:
        item_data["radius"] = radius
    else:
        item_data["radius"] = 100


    #フォームのチェック
    form = ItemModelForm(item_data)
    if form.is_valid() == False:
        for ele in form.errors:
            print(ele)

    data = {"jsonData":json.dumps(item_data, ensure_ascii=False)}

    return data






def create_item_for_android_test(key, data):
    """機能

    Args:
        user_obj: User ... 
        item_data:dict ... create_item_data()を引数として使える。

    Returns:
        item_obj: Item
    """
    #print("ITEM_DATA")

    #print(item_data)
    #print(type(item_data))


    CREATE_ITEM_URL = "/api/item_create_1/"
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + key)
    response = client.post(CREATE_ITEM_URL, data)
    #print(response.status_code)
    #dictItem_data = json.loads(item_data)
    dictItem_data = json.loads(data["jsonData"])

    item_obj = Item.objects.get(title=dictItem_data["title"])
    return item_obj
    










'''
def create_user_with_username_for_test(data):
    """機能
    ユーザー登録を入力として生成したUserオブジェクト,Profileオブジェクトを返す

    Args:
        data:dict ...ユーザー作成用のデータ ex. data = {"email":"postuser@gmail.com", "password1":"12345", "password2":"12345"}
    Returns:
        user_obj: Userオブジェクト
        profile_obj Ptofileオブジェクト
    """

    CREATE_USER_URL = reverse(ViewName.SIGN_UP)
    client = Client()
    client.post(CREATE_USER_URL, data)
    user_obj = User.objects.get(emailaddress=data["email"])
    profile_obj = Profile.objects.get(user=user_obj)
    return user_obj, profile_obj
'''
