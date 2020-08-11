import platform
import os
from avisos.models import Aviso
from profiles.models import Profile
from prefecturas.models import Departamento
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.geos import GEOSGeometry



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





#########################################################
##          Wktをpoint値に変更する関数                    ##
#########################################################

# ブラウザ、android端末から送信される地理情報はwell known textである。
# これをジオメトリ型データに変換する関数を以下とする。
# 使用する場面は 記事作成時、記事編集時、プロフィール編集時である。


def wkt2point(wkt):
    """
    Args:
        wkt: str...Well Known Text (すべてpoint値に関するデータである)
    Returns:
        point: ジオメトリ型 (すべてpoint型のジオメトリデータが返る)

    注: 
    原因が分からないが、環境をDockerを使う場合と使わない場合でwktの値が変わってしまう現象が見られた。
    したがってDockerとそれ以外でpointオブジェクトを生成する方法を変える仕組みに変更する
    またデータオブジェクトを生成するときはこのpoint値を使ってはいけない現象も確認された。。。
    """
    launch_env = os.environ.get("LAUNCH_ENV", default="NO_DOCKER")
    print(launch_env)
    if launch_env == "DOCKER":
        lng = wkt.split(" ")[1].replace("(", "")
        lat = wkt.split(" ")[2].replace(")", "")
        text = "POINT(" + lat + " " + lng + ")"
        point = GEOSGeometry(text)
    elif launch_env == "NO_DOCKER":
        #point  = GEOSGeometry(wkt)
        lng = wkt.split(" ")[1].replace("(", "")
        lat = wkt.split(" ")[2].replace(")", "")
        text = "POINT(" + lat + " " + lng + ")"
        point = GEOSGeometry(text)
    return point



########################################################
###          point値のバリデーション関数                  ##
########################################################

#記事作成時、記事編集時、プロフィール編集時にpoint値を地図から取得する機能がある。
#地図からpoint値を取得する時guatemala領域外の場合にはデータベースに当該point値を登録するのは望ましくない。
#したがって領域外かどうかを判定する関数を以下とする。

def is_in_Guatemala(wkt):
    """機能
    戻り値がTrueの場合pointが示すデータはguatemala内に存在するデータであり、
    Falseの場合は存在しないデータである。
    """
    point = wkt2point(wkt)
    # pointが各departamentoに含まれているかチェックする/含まれればresultをTrueに変更する
    print("そもそもココ通る？？")
    dep_objects = Departamento.objects.all()
    for dep in dep_objects:
        print("within調査")
        print(dep.geom.contains(point))
        if dep.geom.contains(point):
            return True

    return False





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



    