

class SerializerContextKey(object):
    """
    このkeyは、Androidのretrofitのresponse解析に使われる。重要。
    """

    AUTH_TOKEN_KEY = "key" 
    BTN_CHOICE = "BTN_CHOICE"
    ADM0_LIST = "ADM0_LIST"
    ADM1_LIST = "ADM1_LIST"
    ADM2_LIST = "ADM2_LIST"
    IMAGE1 = "IMAGE1"
    IMAGE2 = "IMAGE2"
    IMAGE3 = "IMAGE3"
    ITEM_OBJ = "ITEM_OBJ"
    ITEM_OBJECTS = "ITEM_OBJECTS" 
    SOLICITUD_OBJECTS_SERIALIZER = "SOLICITUD_OBJECTS_SERIALIZER" 
    DM_CONTENT_OBJECTS_SERIALIZER = "DM_CONTENT_OBJECTS_SERIALIZER"
    ITEM_OBJECTS_COSAS      = "ITEM_OBJECTS_COSAS"
    ITEM_OBJECTS_HABITACION = "ITEM_OBJECTS_HABITACION"
    ITEM_OBJECTS_TRABAJO    = "ITEM_OBJECTS_TRABAJO"
    ITEM_OBJECTS_TIENDA     = "ITEM_OBJECTS_TIENDA"



class BtnChoice(object):

    #ユーザー認証されていない場合
    ANONYMOUS_USER_ACCESS = "ANONYMOUS_USER_ACCESS"
    
    #ユーザー認証され、ユーザーが出品者の場合 && 申請者を選ぶ場合
    SELECT_SOLICITUDES = "SELECT_SOLICITUDES"
    #ユーザー認証され、ユーザーが出品者の場合 && 申請者がいない場合
    NO_SOLICITUDES = "NO_SOLICITUDES"

    #ユーザー認証され、ユーザーが出品者の場合 && 取引相手が決まっている場合
    GO_TRANSACTION = "GO_TRANSACTION"



    #ユーザー認証され、ユーザーが出品者以外の場合
    SOLICITAR = "SOLICITAR"
    SOLICITADO = "SOLICITADO"

    #ユーザー認証され、ユーザーが出品者以外のの場合 && 取引相手が決まっている場合(重複しているので情報を削除)
    #GO_TRANSACTION = "GO_TRANSACTION"
    CANNOT_TRANSACTION = "CANNOT_TRANSACTION" #申請者を他の人に決められた時に表示する



# categories/models.py にカテゴリーの値がある。
class CategoryValue(object):

    DONAR_VENDER         = "1"
    BUSCAR_AYUDA         = "2"
    ANUNCIATE            = "3"
    BUSCAR_HABITACION    = "4"
    ALQUILAR_HABITACION  = "5"
    BUSCAR_TRABAJO       = "6"
    BUSCAR_TRABAJADOR    = "7"
    NUESTRA_TIENDA_Y_SERVICIO = "8"



class FirebaseCloudMessagingCase(object):

    ITEMCONTACT_ADDED_TO_ITEM = "ITEMCONTACT_ADDED_TO_ITEM"
    CREATED_SOLICITUD         = "CREATED_SOLICITUD"
    CREATED_DIRECTMESSAGE     = "CREATED_DIRECTMESSAGE"
    CREATED_DM_CONTENT        = "CREATED_DM_CONTENT"








