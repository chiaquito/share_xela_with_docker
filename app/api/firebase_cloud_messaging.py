import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
import os
from config.settings.base import BASE_DIR
from api.models import DeviceToken
from api.constants import FirebaseCloudMessagingCase


#print(os.getcwd())
FILE_NAME = "share-xela-firebase-adminsdk-6a3za-4d5f9d4d35.json"  



class FireBaseMassagingDeal(object):

    '''使用例

    fcmd_obj = FireBaseMassagingDeal()
    fcmd_obj.getDeviceToken(userObj)
    fcmd_obj.makeNotification(strTitle="タイトルです", strBody="通知内容です")
    fcmd_obj.makeMessage(self)
    fcmd_obj.sendMessage(self)

    '''


    def __init__(self):
        self.deviceToken  = None
        self.notification = None
        self.message      = None
        
        #FirebaseAdminSDKの初期化を実施する
        FILE_PATH = BASE_DIR + os.path.join("/config/settings/", FILE_NAME)
        cred = credentials.Certificate(FILE_PATH)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        


    
    def initFirebaseAdminSDK(self):
        """
        FirebaseAdminSDKの初期化を実施する
        基本的にFireBaseMassagingDealを初期化する時に実施されるので使うことはないと思われる
        """
        #FILE_PATH = os.path.join(BASE_DIR, "/config/settings/", FILE_NAME)
        FILE_PATH = BASE_DIR + os.path.join("/config/settings/", FILE_NAME)
        print(FILE_PATH)
        cred = credentials.Certificate(FILE_PATH)
        firebase_admin.initialize_app(cred)

    



    def getDeviceToken(self, userObj):
        """機能
        DjangoのモデルからdeviceTokenを取得する

        Args:
            userObj: django.contrib.auth.models.Userオブジェクト

        Returns:
            str: deviceTokenの文字列を返す
        """

        try:
            deviceToken = DeviceToken.objects.get(user=userObj).device_token
            #deviceToken = "eo99uJ5qAsQ:APA91bHYPfj6LaEF6IcmQzTDEw9FLQigGaVWMGvKBOfVjnb8jjcuarMFr9ae7T1_H0XHJap8S5AONCTQqqTun6kRD7v8ps3fwQ3yH_Ld-WFM2vwqEkFYo790_SOys4vQ1Vqr2UdZ3gnP"
            #print("deviceToken取得成功")
        except:
            deviceToken = None
        
        self.deviceToken = deviceToken



    def makeNotification(self, case=None, data=None):
        """
        Notificationオブジェクトを生成する。
        
        Args:
            case: str
        Returns:
            -
        """
        """テスト項目
        makeNoticationメソッドにdataが渡された時そのbodyとしてitemオブジェクトのタイトルが表示される
        """
        if case == None:
            strTitle = 'test server'
            strBody = 'test server message'

        elif case == FirebaseCloudMessagingCase.ITEMCONTACT_ADDED_TO_ITEM:
            strTitle = "Tiene un comentario sobre el artículo que publicó" #'投稿した記事にコメントが付きました'
            strBody  = "sharexela"  #data["item_obj"]
        elif case == FirebaseCloudMessagingCase.CREATED_SOLICITUD:
            strTitle = "Ha recibido propuestas para su artículo" #"投稿した記事に対して応募がありました"
            strBody  = "sharexela" #data["item_obj"]   # "Usernameを記述する"
        elif case == FirebaseCloudMessagingCase.CREATED_DIRECTMESSAGE:
            strTitle = "Ha sido seleccionado para hacer negocios sobre este articulo." #"取引相手としてあなたが決まりました"
            strBody  = "sharexela" #data["item_obj"]   # "投稿記事タイトルを表示します"
        elif case == FirebaseCloudMessagingCase.CREATED_DM_CONTENT:
            strTitle = "Su mensaje ha sido recibido." #"メッセージが届きました"
            strBody  = "sharexela" #data["item_obj"] #"メッセージ内容を表示する"


        notification=messaging.Notification(
            title = strTitle,
            body = strBody,
        )

        self.notification = notification



    def makeMessage(self, data=None):

        message = messaging.Message(
            notification = self.notification,
            token = self.deviceToken,
            data = None
            )
        self.message = message



    def sendMessage(self):
        """
        デバイストークンが得られなかったものは通知を送信しない
        デバイストークンが得られたものだけ通知を送信するプロセスを実行する
        """
        if self.deviceToken == None:
            return #print("deviceTokenなし")
        messaging.send(self.message)
        #print("送信")



    def doPushNotification(self, userObj, case=None):
        """
        まとめたもの
        """

        self.getDeviceToken(userObj)
        self.makeNotification(case=case)
        self.makeMessage()
        self.sendMessage()








 