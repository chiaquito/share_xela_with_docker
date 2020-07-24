
from django.contrib.auth.models import User
from items.models import Item


from config.constants import ContextKey



def addBtnFavToContext(request, item_obj, context):
    """機能
    
    アイテム詳細ページにcontext[btn_fav]を追加する。
    場合によってはcontext[fav_obj_id]も追加する。

    input:
    request: Request
    item_obj:Item 
    context: dict
    
    output: dict
    用途:
    ItemDetailView#getにのみ使われる

    """
    """
    テスト項目
    item.favorite_usersに格納されるすべてのUserオブジェクトをusers: listに格納できている 
    既にfavボタンを押しているユーザーのアクセスの場合fav_objはNoneではない。 fav_objはUserオブジェクトである
    未認証ユーザーの場合にはcontext["btn_fav"]の値が"NO_SHOW"である。
    アイテムにfavを押している認証ユーザーの場合にはcontext["fav_obj_id"]というキーが存在しない。
    アイテムにfavを押している認証ユーザーの場合にはcontext["btn_fav"]の値が"RED_HEART"である。
    アイテムにfavを押している認証ユーザーの場合にはcontext["fav_obj_id"]というキーが存在する。
    アイテムにfavを押している認証ユーザーの場合にはcontext["fav_obj_id"]の値はFavoriteオブジェクトのidである
    アイテムにfavを押していない認証ユーザーの場合にはcontext["btn_fav"]の値が"WHITE_HEART"である。
    アイテムにfavを押していない認証ユーザーの場合にはcontext["fav_obj_id"]というキーが存在する。
    アイテムにfavを押していない認証ユーザーの場合にはcontext["fav_obj_id"]の値は"NO_ID"である
    """


    # context["btn_fav"]を設定
    if request.user.is_anonymous:
        #print("ANONYMOUS_USERなのでCONTEXTにNO_SHOWを追加するが、この値はテスト以外に使われることはない")
        context[ContextKey.BTN_FAV] = "NO_SHOW"
        return context

    access_user = User.objects.get(username=request.user.username)

    for fav_user in item_obj.favorite_users.all():
        if fav_user == access_user:
            context[ContextKey.BTN_FAV] = "RED_HEART"
            return context

    context[ContextKey.BTN_FAV] = "WHITE_HEART"
    return context







def addBtnFavToContext_botsu(request, item_obj, context):
    """機能
    
    アイテム詳細ページにcontext[btn_fav]を追加する。
    場合によってはcontext[fav_obj_id]も追加する。

    input: 
    context: dict
    request: Request

    output: dict
    用途:
    ItemDetailView#getにのみ使われる

    """
    """
    テスト項目
    item.favorite_usersに格納されるすべてのUserオブジェクトをusers: listに格納できている 
    既にfavボタンを押しているユーザーのアクセスの場合fav_objはNoneではない。 fav_objはUserオブジェクトである
    未認証ユーザーの場合にはcontext["btn_fav"]の値が"NO_SHOW"である。
    アイテムにfavを押している認証ユーザーの場合にはcontext["fav_obj_id"]というキーが存在しない。
    アイテムにfavを押している認証ユーザーの場合にはcontext["btn_fav"]の値が"RED_HEART"である。
    アイテムにfavを押している認証ユーザーの場合にはcontext["fav_obj_id"]というキーが存在する。
    アイテムにfavを押している認証ユーザーの場合にはcontext["fav_obj_id"]の値はFavoriteオブジェクトのidである
    アイテムにfavを押していない認証ユーザーの場合にはcontext["btn_fav"]の値が"WHITE_HEART"である。
    アイテムにfavを押していない認証ユーザーの場合にはcontext["fav_obj_id"]というキーが存在する。
    アイテムにfavを押していない認証ユーザーの場合にはcontext["fav_obj_id"]の値は"NO_ID"である
    """

    fav_obj = None
    users   = []


    # context["btn_fav"]を設定
    if request.user.is_anonymous:
        print("ANONYMOUS_USERなのでCONTEXTにNO_SHOWを追加するが、この値はテスト以外に使われることはない")
        context[ContextKey.BTN_FAV] = "NO_SHOW"
        return context



    request_user = User.objects.get(username=request.user.username)

    for fav in item_obj.favorite_users.all():
        users.append(fav.user)
        if fav.user == request_user:
            fav_obj = fav



    if request.user.is_authenticated and request_user not in users:
        #白のハートボタンを表示するためにcontextを追加する
        print("白のハートボタンを表示するためにcontextを追加する")
        context[ContextKey.BTN_FAV] = "WHITE_HEART"
        context["fav_obj_id"] = "NO_ID"
        return context

    elif request.user.is_authenticated and request_user in users:
        #赤のハートボタンを表示するためにcontextを追加する
        print("赤のハートボタンを表示するためにcontextを追加する")
        context[ContextKey.BTN_FAV] = "RED_HEART"
        # htmlに<input name="fav_obj_id" value={{ fav_id }}>を追加するするための処理を行う
        context["fav_obj_id"] = fav_obj.id
        return context
