import platform
import os
from avisos.models import Aviso
from profiles.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



################################################
##   ページネーションに関する関数を設定             ##
################################################
# https://docs.djangoproject.com/ja/2.2/topics/pagination/#module-django.core.paginator

def paginate_queryset(request, queryset, count=12):
    """機能
    views.py内にPaginatorオブジェクトを組み込むことでページネーションを実装させる。
    またテンプレートで使用するためのPageオブジェクトを返り値として返す。
    Pageオブジェクトを返す。

    Args:
        request:Request... Requestオブジェクト
        queryset:QuerySet... 分割表示したいオブジェクトの総オブジェクト
        count: Int... 1ページ当たり表示するオブジェクト数 なければデフォルト値20が使われる
    Returns:
        page_obj:Page  https://docs.djangoproject.com/ja/2.2/topics/pagination/#paginator-objects

    使用先：
        各カテゴリーの結果表示、ユーザー別記事表示、Favorit記事表示、Avisoの各通知リスト
    
    ページネーションコンポーネント：
        {% include '' %}

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj




########################################################
###   navbarに通知を表示させるためのオブジェクトを取得する  ####
########################################################


def add_aviso_objects(request, context):
    """
    navbarに表示させるavisoオブジェクトをcontextに追加する
    
    """
    if request.user.is_anonymous == True:
        return context
    elif Profile.objects.filter(user=request.user).exists() == False :
        return context
    aviso_objects = Aviso.objects.filter(aviso_user=Profile.objects.get(user=request.user)).filter(checked=False)
    context["aviso_objects"] = aviso_objects
    context["aviso_count"] = aviso_objects.count()
    return context






################################################
### runserver の環境変数を自動設定               ##
################################################

OS = ""
OS_TYPE = ["OSX", "LINUX"]


def getTypeOS():
    """
    'python manage.py runserver' コマンド実行時のOSを判定する。

    Returns:
        str: OSXまたはLINUXの文字列
    """

    pf = platform.system()

    if pf == 'Darwin':
        print("OSXの環境 -> 開発環境")
        OS = OS_TYPE[0]
        return OS

    if pf == 'Linux':
        print("LINUXの環境 -> 製品環境")
        OS = OS_TYPE[1]
        return OS
    


def setDjangoSettingsModule(OS):
    """
    OS(開発環境、製品環境)によって、 'DJANGO_SETTINGS_MODULE' を定める。
    これにより、 python manage.py runserver --settings DJANG0_SETTINGS_MODULE=config.settings.dev_settings
    と入力する必要がなくなる。
    単に python manage.py runserver コマンドを実行すれば良い
    """

    if OS == OS_TYPE[0]:
        return os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev_settings')

    if OS == OS_TYPE[1]:
        return os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod_settings')



def setDSM():
    OS = getTypeOS()
    return setDjangoSettingsModule(OS)



    