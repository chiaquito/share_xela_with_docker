from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Contact(models.Model):
	"""
	問い合わせオブジェクトのモデル
	"""
	title_choice  = (
		#("会員登録、ログインについて","会員登録、ログインについて"),
		#("投稿方法・投稿ルールについて", "投稿方法・投稿ルールについて"),
		#("ユーザー間のトラブルについて", "ユーザー間のトラブルについて"),
		#("その他", "その他"),
		("Como registrarte e inicio de sesión","Como registrarte e inicio de sesión"),
		("Método de publicación / reglas de publicación", "Método de publicación / reglas de publicación"),
		("Probemas entre usuarios", "Probemas entre usuarios"),
		("Otros", "Otros"),
			) 

	#user          = models.ForeignKey(User, on_delete=models.PROTECT, null=True )
	title         = models.CharField(choices=title_choice ,max_length=60)
	email_address = models.EmailField() 
	content       = models.TextField()

	def __str__(self):
		return " : "+str(self.title)
