


### Context ###
class ContextKey(object):
    ITEM_OBJECTS = "item_objects"
    BTN_CHOICE   = "btn_choice"
    BTN_FAV      = "btn_fav"


    


class ContextValue(object):
    pass





### Templates ###
class TemplateKey(object):
    """
    近いうち削除する
    """
    HOME        = "config/home_kaizen.html"
    ITEM_DETAIL = "items/detail_item2.html"
    ITEM_LIST   = "items/list_items.html"
    NO_ITEMS    = "items/no_item.html"


class TemplateName(object):
    HOME        = "config/home_kaizen.html"
    ITEM_DETAIL = "items/detail_item2.html"
    ITEM_LIST   = "items/list_items.html"
    NO_ITEMS    = "items/no_item.html" 
    DIRECT_MESSAGE_DETAIL = "direct_messages/dm_detail.html"
    SOLICITUD_INPUT = "solicitudes/input_form.html"
    SOLICITUD_LIST  = 'solicitudes/solicitud_decision.html'
    


## ViewName ##
class ViewName(object):
    HOME        = "home"
    SIGN_UP     = "account_signup" # https://django-allauth.readthedocs.io/en/latest/views.html
    ITEM_DETAIL = 'items:item_detail'
    ITEM_FAVORITE = 'items:item_favorite'
    ITEM_LIST_BY_FAVORITE = 'items:item_list_by_favorite'
    ITEM_CONTACT     = 'item_contacts:ItemContactView'
    ITEM_CREATE = "items:item_create2"

    DIRECT_MESSAGE_DETAIL = 'direct_messages:dm_detail'
    FEEDBACK_CREATE  = 'feedback:feedback'
    SOLICITUD_INPUT  = "solicitudes:solicitud_input"
    SOLICITUD_LIST   = "solicitudes:solicitud_list"
    SOLICITUD_SELECT = "solicitudes:solicitud_decision"

    ItemContactListByContactObjPKAPIView = "api:ItemContactListByContactObjPKAPIView"

