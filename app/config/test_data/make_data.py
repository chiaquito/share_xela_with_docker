from items.models import Item
from config.settings.dev_settings import DEBUG
import random

from django.contrib.auth.models import User
from items.models import Item
from categories.models import Category
from avisos.models import Aviso
from feedback.models import Feedback
from profiles.models import Profile
from prefecturas.models import RegionClassed
from api.models import DeviceToken


print("スクリプトを実行")
"""
python manage.py shell
from config.test_data.make_data import main

main()
"""






INSTALLED_APPS_FOR_TEST_DATA = [
    'feedback',

    'avisos',
    'api',
    'categories',
    'contacts',
    'direct_messages',
    'favorite',
    
    'maps',
    'mypages',
    'item_contacts',
    'items',
    'prefecturas',
    'profiles',
    'solicitudes',    
]



title_cosa_list =[
        'libros de medicina',
        'bota',
        'televisión',
        'mesa',
        'cama',
        'ordenador',
        'mesa',
        'camara',
        'libro',
        'silla',
        'luz',
        'ropa',
        'ropa segunda mano',
        'uniforme para primaria',
        'golla',
        'zapatos de fútbol',
        'pelota',
        'juguete',
        'lápiz de memoria USB',
        'teléfono móvil',
        'teléfono',
        'teléfono',
        'moto',
]

title_aviso_list = [
        'grupo que les encanta escalar montañas.',
        'La mascota de mi perro se ha ido.',
        '¿Te gustaría estudiar ruso con nosotros?',
        'Mañana una batalla de rap en el parque.',

]


title_habitacion_alquilar_list =[

        'hay una habitación disponible. Es espacioso.',
        'Tenemos habitaciones cerca  de San Carlos.',
        'habitación cerca del mercado de Democracia.',
        'habitación disponible. Las comidas servidas.',
        'Es una casa de muchos estudiantes.',
        'habitación disponible. Aceptamos viajeros.',
]

title_habitacion_buscar_list =[
        'buscando una habitación cerca de San Carlos.',
        'buscando una habitación barata.',
        'habitación para alojar a los viajeros.', 
]




description_sample = """
Este artículo es una muestra. Se eliminará cuando los usuarios escriban más artículos.

Si quieres regalar algo que no quieres a otra persona, puedes usar la categoría
Elija "1 : Gente que quiere donar o vender" para crear un artículo. Introduzca el valor de cesión que desee.

Si quieres que alguien te regale un objeto específico o necesitas la ayuda de alguien, usa "2 : Gente que busca donante".

Si está buscando a su mascota o si la ha perdido, elija "3 : Gente que quiere Elija "avisar". 
Si está buscando miembros de la comunidad de estudio de otros idiomas,
o si está buscando un grupo de alpinistas, elija "avisar". también está en la misma categoría. Esta es también la categoría para anunciar un evento de algún tipo.

Si está buscando una habitación, puede usar "4 : Gente que busca una habitación" 
Por favor, seleccione una categoría y describa su criterio deseado.

Si está buscando una habitación para alquilar, puede escribir "5 : Gente que alquila una Elija "habitación".

Si está buscando trabajo, elija 6 : Gente que busca trabajo. Es una buena idea describir lo que puedes hacer.

Si busca un trabajador, elija "7 : Gente que busca trabajador". 



                     """

description_sample_ja = """
この記事はサンプルです。利用者の記事が増えたら削除されます。

自分のいらないものを誰かに譲りたい場合はカテゴリーの
"1 : Gente que quiere donar o vender"を選んで記事を作成します。希望の譲り値を入力してください。
誰かから特定の物を譲ってほしい場合や誰かの助けを必要としている場合には、"2 : Gente que busca donante"を選んでください。
自分のペットがいなくなったりして探している場合は"3 : Gente que quiere avisar"を選んでください。その他にも外国語の勉強コミュニティメンバーを探していたり、山登りのメンバーを集める場合も同じカテゴリーです。何かのイベントを告知する場合もこのカテゴリーです。
部屋を探している場合には"4 : Gente que busca una habitación"のカテゴリーを選んで希望する条件を記述してください。
部屋を借りる人を探している場合には"5 : Gente que alquila una habitación"を選んでください。
仕事を探している人は6 : Gente que busca trabajoを選んでください。具体的に何ができるかを書くと良いと思います。
労働者を探している場合には"7 : Gente que busca trabajador"を選んでください。
"""






class TestData(object):

    def delete_objects(self):
        DeviceToken.objects.all().delete()
        Feedback.objects.all().delete()
        Aviso.objects.all().delete()
        Profile.objects.filter(user__is_superuser=False).delete()
        Item.objects.all().delete()
        User.objects.all().filter(is_superuser=False).delete()


    def load_set_up(self):
        from config.set_up import main
        main()

    def make_users(self):

        try:
            chiaki = User.objects.create(username="chiaki_1", email="chiaki@zzzmail.com", password="12345")
            rc_obj = random.choice(RegionClassed.objects.all())
            adm2 = random.choice(rc_obj.municipios.all()).adm2_es
            profile_obj = Profile.objects.get(user=chiaki)
            profile_obj.adm1 = rc_obj.departamento.adm1_es
            profile_obj.adm2 =adm2
            profile_obj.save()
        except:
            print("error")
            pass
        try:    
            yan = User.objects.create(username="yan", email="yan@zzzmail.com", password="12345")
            rc_obj = random.choice(RegionClassed.objects.all())
            adm2 = random.choice(rc_obj.municipios.all()).adm2_es
            profile_obj = Profile.objects.get(user=yan)
            profile_obj.adm1 = rc_obj.departamento.adm1_es
            profile_obj.adm2 =adm2
            profile_obj.save()            
        except:
            print("error")
            pass
        try:
            tom = User.objects.create(username="tom", email="tom@zzzmail.com", password="12345")
            rc_obj = random.choice(RegionClassed.objects.all())
            adm2 = random.choice(rc_obj.municipios.all()).adm2_es
            profile_obj = Profile.objects.get(user=tom)
            profile_obj.adm1 = rc_obj.departamento.adm1_es
            profile_obj.adm2 =adm2
            profile_obj.save()                        
        except:
            print("error")
            pass
        try:
            taka = User.objects.create(username="taka", email="taka@zzzmail.com", password="12345")
            rc_obj = random.choice(RegionClassed.objects.all())
            adm2 = random.choice(rc_obj.municipios.all()).adm2_es
            profile_obj = Profile.objects.get(user=taka)
            profile_obj.adm1 = rc_obj.departamento.adm1_es
            profile_obj.adm2 =adm2
            profile_obj.save()                        
        except:
            print("error")
            pass

    def make_items(self):
        #data_template = {user, title, description, price, category, adm0, adm1, adm2, point, radius, }
        
        for num in range(60):
            data = {}
            user_obj = random.choice(User.objects.all())
            data["user"] = user_obj
            category_obj = random.choice(Category.objects.all())
            data["category"] = category_obj
            if category_obj.number == "1" or category_obj.number == "2":
                title = random.choice(title_cosa_list)
                data["title"] = title
            elif category_obj.number == "3":
                title = random.choice(title_aviso_list)
                data["title"] = title
            elif category_obj.number == "4":
                title = random.choice(title_habitacion_buscar_list)
                data["title"] = title
            elif category_obj.number == "5":
                title = random.choice(title_habitacion_alquilar_list)
            

            else:
                continue
            description = description_sample
            data["description"] = description

            profile_obj = Profile.objects.get(user=user_obj)
            itemobj = Item.objects.create(user=user_obj, category=category_obj, title=title, description=description, adm0="GUATEMALA", adm1=profile_obj.adm1, adm2=profile_obj.adm2 )
            



def main():
    if DEBUG == True:
        td_obj = TestData()
        td_obj.delete_objects()
        td_obj.load_set_up()
        td_obj.make_users()
        td_obj.make_items()
        #td_obj.make_users()

        



if __name__ == '__main__':
    main()