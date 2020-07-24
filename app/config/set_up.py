#デプロイしたら毎回行うスクリプト
#from config.set_up import main


from prefecturas.models import Prefectura, Departamento, Municipio, RegionClassed
from prefecturas.load import PrefecturaInstanceMaker, MunicipioInstanceMaker, DepartamentoInstanceMaker, RegionClassedInstanceMaker
from categories.models import CATEGORY_CHOICE, Category




def main():

    #Prefecturaインスタンスの生成
    if Prefectura.objects.all().count() == 0:
        obj = PrefecturaInstanceMaker()
        obj.showReadingSource()
        obj.run()

    #Departamentインスタンスの生成
    if Departamento.objects.all().count() == 0:
        obj = DepartamentoInstanceMaker()
        obj.showReadingSource()
        obj.run()

    #Municipioインスタンスの生成
    if Municipio.objects.all().count() == 0:
        obj = MunicipioInstanceMaker()
        obj.showReadingSource()
        obj.run()

    #RegionClassedインスタンスの生成
    if RegionClassed.objects.all().count() == 0:
        RegionClassedInstanceMaker().departamentoRelatedMunicipio()


    #Categoryインスタンスの作成
    for ele in CATEGORY_CHOICE:
        value = ele[0]
        if Category.objects.filter(number=value).exists() != True:
            Category.objects.create(number=value)



if __name__=="__main__":
    main()






