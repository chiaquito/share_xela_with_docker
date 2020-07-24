from django.db import models

# Create your models here.


CATEGORY_CHOICE = (

    ("1",  "quiero donar o vender"),
    ("2",  "quiero buscar donante"),
    ("3",  "quiero avisar"),
    ("4",  "quiero buscar una habitación"),
    ("5",  "quiero alquilar una habitación"),
    ("6",  "quiero dar pensionado"),
    ("7",  "quiero buscar pensionista"),
    ("8",  "quiero buscar empleado"),
    ("9",  "quiero buscar trabajador"),
    ("10", "publicidad de Enpresas y Servicios")


    )


###################
"""

999 ---すべてのアイテムを取得する
500 --- Las Cosas...(1,2,3) dar o donar, busca donante, quiere avisarのカテゴリを一括にしたもの
600 --- Habitacion...(4,5,6,7) buscar habitacion, alquilar habitacion, dar pencionado, busco pencionista
700 --- trabajo ...(8,9) buscar empleo, buscar trabajador
800 ___ Empresas y Servicios ...(10) publicidad de Enpresas y Servicios

"""



#("dar,vender","dar,vender"),("querer", "querer"),("anuncio", "anuncio"),

class Category(models.Model):
    number = models.CharField(max_length=30, choices=CATEGORY_CHOICE, unique=True) #, unique=True


    def __str__(self):
        #return self.number
        return "{} : {}".format(self.number, self.get_number_display())


