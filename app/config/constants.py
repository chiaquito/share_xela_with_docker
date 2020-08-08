

### Context ###
class ContextKey(object):
    """
    views.pyにおけるcontextキーのハードコーディングを置き換える
    """    
    ITEM_OBJECTS  = "item_objects"
    BTN_CHOICE    = "btn_choice"
    BTN_FAV       = "btn_fav"
    PAGE_OBJ      = "page_obj"
    AVISO_OBJECTS = "aviso_objects"




### Templates ###
class TemplateName(object):
    """
    views.pyにおけるハードコーディングを置き換える
    """
    # config
    HOME            = "config/home_kaizen.html"
    HOWTO           = 'config/howto.html'
    PRIVACY         = 'config/privacy_es.html'
    CHANGE_USERNAME = 'config/change_username.html'
    CHANGE_EMAIL    = 'config/change_emailaddress.html'
    # items
    ITEM_DETAIL     = "items/detail_item2.html"
    ITEM_LIST       = "items/list_items.html"
    NO_ITEMS        = "items/no_item.html"
    USER_ITEM_LIST  = "items/item_user_list/list.html"
    # direct_messages
    DIRECT_MESSAGE_DETAIL = "direct_messages/dm_detail.html"
    # solicitudes
    SOLICITUD_INPUT = "solicitudes/input_form.html"
    SOLICITUD_LIST  = 'solicitudes/solicitud_decision.html'

    

## ViewName ##
class ViewName(object):
    """
    test, views.pyにけるハードコーディング部分を置き換える 
    """
    # config    
    HOME          = "home"
    HOWTO         = "howto"
    EDIT_USERNAME = "username_change"
    SIGN_UP       = "account_signup" # https://django-allauth.readthedocs.io/en/latest/views.html#signup-account-signup
    ACCOUNT_LOGIN = 'account_login'  # https://django-allauth.readthedocs.io/en/latest/views.html#login-account-login
    # item_contacts
    ITEM_CONTACT  = 'item_contacts:ItemContactView'
    # items
    ITEM_DETAIL   = 'items:item_detail'
    ITEM_FAVORITE = 'items:item_favorite'
    ITEM_LIST_BY_FAVORITE = 'items:item_list_by_favorite'
    ITEM_CONTACT  = 'item_contacts:ItemContactView'
    ITEM_CREATE   = "items:item_create2"
    ITEM_EDIT     = "items:item_edit"
    # direct_messages
    DIRECT_MESSAGE_DETAIL = 'direct_messages:dm_detail'
    FEEDBACK_CREATE  = 'feedback:feedback'
    # solicitudes
    SOLICITUD_INPUT  = "solicitudes:solicitud_input"
    SOLICITUD_LIST   = "solicitudes:solicitud_list"
    SOLICITUD_SELECT = "solicitudes:solicitud_decision"
    # profiles
    PROFILE_EDIT     = "profiles:profile"
    # api
    ItemContactListByContactObjPKAPIView = "api:ItemContactListByContactObjPKAPIView"
    # avisos
    AVISO_ALL        = 'avisos:avisos_alllist'
    AVISO_LIST       = "avisos:avisos_list"

