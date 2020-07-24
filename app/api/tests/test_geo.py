from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
#from api.models import DeviceToken
from django.urls import reverse_lazy


#from prefecturas.functions import departamentoRelatedMunicipio
from prefecturas.models import RegionClassed
from prefecturas.load import DepartamentoInstanceMaker, MunicipioInstanceMaker, RegionClassedInstanceMaker



class GetRegionDataByPointAPIViewTest(TestCase):
    """テスト目的
    """
    """テスト対象
    api/views.py GetRegionDataByPointAPIView#post
    endpoint: api/util/region/
    name: -
    """
    """テスト項目
    pointのwkt値がGuatemala内のQuezaltenangoの場合、adm1値はQuezaltenangoになる。
    pointのwkt値がGuatemala内のQuezaltenangoの場合、adm2値はQuezaltenangoになる。
    pointのwkt値がGuatemala国外のTapachulaの場合、adm1値はNoneになる。
    pointのwkt値がGuatemala国外のTapachulaの場合、adm2値はNoneになる。
    """

    def setUp(self):
        """テスト環境
        Departamentオブジェクトの生成
        Municipioオブジェクトの生成
        RegionClassedオブジェクトの生成
        """
        obj = DepartamentoInstanceMaker()
        obj.run()        
        obj = MunicipioInstanceMaker()
        obj.run()
        RegionClassedInstanceMaker().departamentoRelatedMunicipio()
        access_user  = User.objects.create_user(username="access_user", email="test_access_user@gmail.com", password='12345')
        Token.objects.create(key="TOKEN_VALUE", user=access_user)       


    def test_pointのwkt値がGuatemala内のQuezaltenangoの場合_adm1値はQuezaltenangoになる(self):
        EXPECTED = "Quetzaltenango"
        WKT_POINT = "SRID=4326;POINT (-91.5186882019043 14.840104978041298)"
        WKT_POINT = "SRID=4326;POINT (-91.51643849909306 14.84320911634316)"
        data = {"wkt_point": WKT_POINT}
        token = Token.objects.get(user__username="access_user")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +  token.key)
        response = self.client.post("/api/util/region/", data)
        print(response.status_code)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.data["adm1"], EXPECTED)


    def test_pointのwkt値がGuatemala内のQuezaltenangoの場合_adm2値はQuezaltenangoになる(self):
        EXPECTED = "Quetzaltenango"
        
        WKT_POINT = "SRID=4326;POINT (-91.51643849909306 14.84320911634316)"
        data = {"wkt_point": WKT_POINT}
        token = Token.objects.get(user__username="access_user")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +  token.key)
        response = self.client.post("/api/util/region/", data)
        self.assertEqual(response.data["adm2"], EXPECTED)


    def test_pointのwkt値がGuatemala国外のTapachulaの場合_adm1値はNoneになる(self):
        EXPECTED = None
        
        WKT_POINT = "SRID=4326;POINT (-92.3129813 14.9114382)" #タパチュラの座標
        data = {"wkt_point": WKT_POINT}
        token = Token.objects.get(user__username="access_user")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +  token.key)
        response = self.client.post("/api/util/region/", data)
        self.assertEqual(response.data["adm1"], EXPECTED)       


    def test_pointのwkt値がGuatemala国外のTapachulaの場合_adm2値はNoneになる(self):
        EXPECTED = None
        
        WKT_POINT = "SRID=4326;POINT (-92.3129813 14.9114382)" #タパチュラの座標
        data = {"wkt_point": WKT_POINT}
        token = Token.objects.get(user__username="access_user")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +  token.key)
        response = self.client.post("/api/util/region/", data)
        self.assertEqual(response.data["adm2"] ,EXPECTED)


    def test_pointのwkt値がGuatemala国外の場合_adm1値はNoneになる(self):
        EXPECTED = None
        
        WKT_POINT = "SRID=4326;POINT (-60.7567217 35.0969379)" #大西洋
        data = {"wkt_point": WKT_POINT}
        token = Token.objects.get(user__username="access_user")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +  token.key)
        response = self.client.post("/api/util/region/", data)
        self.assertEqual(response.data["adm1"] ,EXPECTED)
        


