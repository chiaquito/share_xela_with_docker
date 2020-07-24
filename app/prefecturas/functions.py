
from django.core.serializers import serialize
import json

from prefecturas.models import Prefectura
from prefecturas.models import Departamento
from prefecturas.models import Municipio
from prefecturas.models import RegionClassed


from xml.etree.ElementTree import *
from xml.dom import minidom
from config.settings.dev_settings import BASE_DIR



def checkMultiPolygonMunicipio():
    """
    Municipioのgeometry型がMultiPolygonなので穴あきポリゴンであるか、シンプルポリゴンか確認するための関数
    """

    municipios = Prefectura.objects.all()
    geojson = serialize('geojson', municipios, geometry_field="mpoly", fields=("mpoly"))
    dicGeojson = json.loads(geojson)
    for number in range(len(dicGeojson["features"])):
        
        municipio = dicGeojson["features"][number]
        #シンプルポリゴンの場合は１、穴開きポリゴンの場合は2以上の数値となる
        countPolygons = str(len(municipio['geometry']['coordinates'][0]))
        #外側のポリゴンの座標点の構成要素数
        countOutlinePolygonElement = str(len(municipio['geometry']['coordinates'][0][0]))
        #座標点の構成要素数　：　通常は２点
        countCoordinate = str(len(municipio['geometry']['coordinates'][0][0][0]))

        print("NUMERO   :    " + str(number) + "   のチェック")
        print("ポリゴンの構成要素数は　：　" + countPolygons )
        print("外側のポリゴンの座標点構成要素数　：　" + countOutlinePolygonElement)
        print("座標点の要素数(X,Y) : " + countCoordinate)
        print("=========================================================")

        if countPolygons != "1" :
            print("*********************************")
            print("**シングルポリゴンではない要素を発見**")
            print("*********************************")
            return
    print("結果　　：　正常　すべてシングルポリゴンである")







#############################################
##        Android Studio用スクリプト         ##
#############################################
 

#string.xmlでDepartamento, Municipioオブジェクトの一覧を作成したい


#仕様 Paisの場合
"""
<string-array name="paisList">
    <item>GUATEMALA</item>
    <item>OTROS</item>
</string-array>

"""


def output_xml_departamentos():


    string_array = Element('string-array', {"name":"departamentoList"})
    objects = Departamento.objects.all()
    adm1_list = sorted([obj.adm1_es for obj in objects])
    
    for n in range(len(adm1_list)):
        item = SubElement(string_array, 'item')
        item.text = adm1_list[n]

    tree = ElementTree(string_array).getroot()
    output_file = BASE_DIR + '/' + "prefecturas/" + "xml/" +'departamento_list.xml'  
    document = minidom.parseString(tostring(tree, 'utf-8'))
    file = open(output_file, 'w')
    # エンコーディング、改行、全体のインデント、子要素の追加インデントを設定しつつファイルへ書き出し
    document.writexml(file, encoding='utf-8', newl='\n', indent='', addindent='  ')
    file.close()




def output_xml_municipios():


    string_array = Element('string-array', {"name":"municipioList"})
    objects = Municipio.objects.all()
    adm2_list = sorted([obj.adm2_es for obj in objects])

    for n in range(len(adm2_list)):
        item = SubElement(string_array, 'item')
        item.text = adm2_list[n]
      
 
    tree = ElementTree(string_array).getroot()
    output_file = BASE_DIR + '/' + "prefecturas/" + "xml/" +'municipio_list.xml'  
    document = minidom.parseString(tostring(tree, 'utf-8'))
    file = open(output_file, 'w')
    # エンコーディング、改行、全体のインデント、子要素の追加インデントを設定しつつファイルへ書き出し
    document.writexml(file, encoding='utf-8', newl='\n', indent='', addindent='  ')
    file.close()



def output_xml_municipios_by_departamentos():
    #from prefecturas.functions import output_xml_municipios_by_departamentos


    rc_deps = RegionClassed.objects.distinct("departamento")
    for rc in rc_deps :

        rc_munis = rc.municipios.all()
        print("##############")
        print("<<<<", rc.departamento)
        list_name = rc.departamento
        caja = []
        for muni in  rc_munis:
            print(muni)
            caja.append(muni.adm2_es)
        print("==============")

        print(caja)



