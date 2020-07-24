
import os
from django.contrib.gis.utils import LayerMapping
from .models import Prefectura
from .models import Municipio
from .models import Departamento
from .models import RegionClassed







class PrefecturaInstanceMaker(object):

	""" *使用方法*

	python manage.py shell
	from prefecturas.load import PrefecturaInstanceMaker

	obj = PrefecturaInstanceMaker()
	obj.showReadingSource()
	obj.run()

	"""

	shp_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'data', 'municipio','gtm_admbnda_adm2_ocha_conred_20190207.shp' ))
	#shp_file = "C:\\Users\\USER\\Dropbox\\geodjango\\prefecturas\\data\\gtm_admbnda_adm2_ocha_conred_20190207.shp"

	prefectura_mapping = {
		'shape_leng' : 'Shape_Leng',
		'shape_area' : 'Shape_Area',
		'adm2_es'    : 'ADM2_ES',
		'adm2_pcode' : 'ADM2_PCODE',
		'adm2_ref'   : 'ADM2_REF',
		'adm2alt1es' : 'ADM2ALT1ES',
		'adm2alt2es' : 'ADM2ALT2ES',
		'adm1_es'    : 'ADM1_ES',
		'adm1_pcode' : 'ADM1_PCODE',
		'adm0_es'    : 'ADM0_ES',
		'adm0_pcode' : 'ADM0_PCODE',
		'date'       : 'date',
		'validon'    : 'validOn',
		'validto'    : 'validTo',
		'mpoly'      : 'MULTIPOLYGON'
		}

		#'mpoly'      : 'POLYGON',
		#}


	def showReadingSource(self):
		print("PATH : ",self.shp_file)
		return 

	def run(self):
		if Prefectura.objects.all().count() != 0:
			print("すでにインスタンスが生成されています")
			return 
		lm = LayerMapping(Prefectura, self.shp_file, self.prefectura_mapping, transform=True, encoding='UTF-8')
		lm.save(strict=False, verbose=True)
		print("Prefecturaインスタンスの生成が完了しました。")
		return 






class MunicipioInstanceMaker(object):


	""" *使用方法*

	python manage.py shell
	from prefecturas.load import MunicipioInstanceMaker

	obj = MunicipioInstanceMaker()
	obj.showReadingSource()
	obj.run()

	"""
	shp_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'data', 'municipio','gtm_admbnda_adm2_ocha_conred_20190207.shp' ))
	#shp_file = "C:\\Users\\USER\\Dropbox\\geodjango\\prefecturas\\data\\gtm_admbnda_adm2_ocha_conred_20190207.shp"

	municipio_mapping = {
		'shape_leng' : 'Shape_Leng',
		'shape_area' : 'Shape_Area',
		'adm2_es'    : 'ADM2_ES',
		'adm2_pcode' : 'ADM2_PCODE',
		'adm2_ref'   : 'ADM2_REF',
		'adm2alt1es' : 'ADM2ALT1ES',
		'adm2alt2es' : 'ADM2ALT2ES',
		'adm1_es'    : 'ADM1_ES',
		'adm1_pcode' : 'ADM1_PCODE',
		'adm0_es'    : 'ADM0_ES',
		'adm0_pcode' : 'ADM0_PCODE',
		'date'       : 'date',
		'validon'    : 'validOn',
		'validto'    : 'validTo',
		'geom'       : 'MULTIPOLYGON'
		}

	def showReadingSource(self):
		return print("PATH : ",self.shp_file)

	def run(self):
		if Municipio.objects.all().count() != 0:			
			return print("すでにインスタンスが生成されています")
		lm = LayerMapping(Municipio, self.shp_file, self.municipio_mapping, transform=True, encoding='UTF-8')
		#lm.save(strict=False, verbose=True)
		lm.save(strict=True, verbose=True)
		
		return print("Municipioインスタンスの生成が完了しました。")



class DepartamentoInstanceMaker(object):
	""" *使用方法*

	python manage.py shell
	from prefecturas.load import DepartamentoInstanceMaker

	obj = DepartamentoInstanceMaker()
	obj.showReadingSource()
	obj.run()

	"""

	shp_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'data', 'departamento','gtm_admbnda_adm1_ocha_conred_20190207.shp' ))

	departamento_mapping = {
		'shape_leng' : 'Shape_Leng',
		'shape_area' : 'Shape_Area',
		'adm1_es'    : 'ADM1_ES',
		'adm1_pcode' : 'ADM1_PCODE',
		'adm1_ref'   : 'ADM1_REF',
		'adm1alt1es' : 'ADM1ALT1ES',
		'adm1alt2es' : 'ADM1ALT2ES',
		'adm0_es'    : 'ADM0_ES',
		'adm0_pcode' : 'ADM0_PCODE',
		'date'       : 'date',
		'validon'    : 'validOn',
		'validto'    : 'validTo',
		'geom'       : 'POLYGON',
	}


	def showReadingSource(self):
		return print("PATH : ",self.shp_file)

	def run(self):
		if Departamento.objects.all().count() != 0:			
			return print("すでにインスタンスが生成されています")
		lm = LayerMapping(Departamento, self.shp_file, self.departamento_mapping, transform=True, encoding='UTF-8')
		#lm.save(strict=False, verbose=True)
		lm.save(strict=True, verbose=True)
		
		return print("Departamentoインスタンスの生成が完了しました。")








class RegionClassedInstanceMaker(object):

	def departamentoRelatedMunicipio(self):
		"""
		from prefecturas.load import RegionClassedInstanceMaker
		RegionClassedInstanceMaker().departamentoRelatedMunicipio()


		"""

		dicDepartamento = {}
		departamentos = Departamento.objects.all()
		for departamento in departamentos:
			dicDepartamento.setdefault(departamento.adm1_pcode, [])
			RegionClassed.objects.create(departamento=departamento)


		#print(dicDepartamento)

		print("=======================================================")

		municipios = Municipio.objects.all()
		for municipio in municipios:
			dicDepartamento[municipio.adm1_pcode].append(municipio.adm2_pcode)

		#print(dicDepartamento)

		#RegionClassedのmunicipiosにデータを追加する。
		for adm1_pcode in dicDepartamento.keys():

			#print(Departamento.objects.get(adm1_pcode=adm1_pcode) ," : ", adm1_pcode)
			#print(dicDepartamento[adm1_pcode])


			depObj = Departamento.objects.get(adm1_pcode=adm1_pcode)
			regionObj = RegionClassed.objects.get(departamento= depObj)
			for adm2_pcode in dicDepartamento[adm1_pcode]:
				municipioObj = Municipio.objects.get(adm2_pcode=adm2_pcode)

				regionObj.municipios.add(municipioObj)

		print("完了")





