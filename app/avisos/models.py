from django.db import models

from django.contrib.auth.models import User

from api.models import DeviceToken
from api.models import DeviceToken
from api.firebase_cloud_messaging import FireBaseMassagingDeal
from api.constants import FirebaseCloudMessagingCase

from items.models import Item
from item_contacts.models import ItemContact
from prefecturas.models import Municipio, Departamento, RegionClassed
from profiles.models import Profile
from solicitudes.models import Solicitud
from direct_messages.models import DirectMessageContent, DirectMessage
from django.db.models.signals import post_save, m2m_changed

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.core.mail import send_mail
import firebase_admin




class Aviso(models.Model):
	'''
	GenericForeignKeyを使うことでitemcontactのやり取りや、direct_messages、申請者が現れたことをAvisoという単一のクラスで表示する。
	これにより各インスタンを時間順に表示させる事ができる	
	'''
	#aviso_user     = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True)
	aviso_user     = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True)
	#aviso_to       = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	content_type   = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True)
	object_id      = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	checked        = models.BooleanField(default=False)
	created_at     = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return str(self.aviso_user)





def sendMail(subject, content, message_to):

	message_from = "from@sharexela.ga"
	send_mail(subject, content, message_from, message_to)




def itemitemcontact_m2m_changed_receiver(sender, instance, action, *args, **kwargs):
	"""機能
	item_obj.item_contactsにItemContactオブジェクトを追加した時に
	通知するユーザー毎にAvisoオブジェクトを生成する。
	"""
	"""テスト項目

	ItemContactオブジェクトが生成されたらItem.item_contacts(ManyToManyField)に当該オブジェクトが追加される。
	ItemContactオブジェクトが生成されたらAvisoオブジェクトが少なくと1つ以上生成される。
	item_m2m_changed_receiver内のitem_contact_objectsが時系列順にItemContactオブジェクトが並んでいる。
	item_contact_objは時系列順に並べたitem_contact_objectsのうち最後のオブジェクトである。
	item_contact_objectsのカウントが0の場合、生成されるAvisoオブジェクトは一つのみである。
	item_contact_objectsのカウントが0の場合、生成されるAvisoオブジェクトのaviso_user値は記事作成者のProfileオブジェクトである。
	item_contact_objectsのカウントが0以外の場合、生成されるAvisoオブジェクトの数はコメント送信者を除く重複なしのpost_userの数またはその数+1である。
	item_contact_objectsのカウントが0以外の場合、生成されるAvisoオブジェクトのaviso_user値はコメント送信者以外のProfileオブジェクトである。
	item_contact_objectsに記事作成者(owner_user)が含まれていない場合、記事作成者がprofilesに含まれる。

	"""
	if action == "post_add":
		
		item_obj = instance
		owner_user = Profile.objects.get(user=item_obj.user)
		item_contact_objects = item_obj.item_contacts.all().order_by('timestamp')
		item_contact_obj = item_contact_objects.last()

		profiles = [item_contact.post_user for item_contact in item_contact_objects]
		profiles.append(owner_user)
		profiles = set(profiles)
		for profile_obj in profiles:
			if profile_obj == item_contact_obj.post_user:
				continue 
			aviso_user = profile_obj
			
			Aviso.objects.create(
				aviso_user=aviso_user,
				content_type=ContentType.objects.get_for_model(item_obj.item_contacts.all().last()),
				object_id=item_obj.item_contacts.all().last().id
				)

			#data = {"item_obj":item_obj.title }

			fcmd_obj = FireBaseMassagingDeal()
			fcmd_obj.getDeviceToken(aviso_user.user)
			fcmd_obj.makeNotification(case=FirebaseCloudMessagingCase.ITEMCONTACT_ADDED_TO_ITEM)
			#fcmd_obj.makeNotification(case=FirebaseCloudMessagingCase.ITEMCONTACT_ADDED_TO_ITEM, data=data)
			fcmd_obj.makeMessage()
			try:
				fcmd_obj.sendMessage()			
			except firebase_admin._messaging_utils.UnregisteredError:
				print("Firebaseのエラー")

			# emailを送信するロジックを挿入
			subject = "ShareXekla Siguió un comentario"
			content = item_obj.title + "\n" 
			message_to = [aviso_user.user.email]
			sendMail(subject, content, message_to)	
		

m2m_changed.connect(itemitemcontact_m2m_changed_receiver, sender=Item.item_contacts.through)





def itemsolicitudes_m2m_changed_receiver(sender, instance, action, pk_set, *args, **kwargs):
	
	"""機能
	item_obj.solicitudesにSolicitudオブジェクトを追加した時に
	通知するユーザーにAvisoオブジェクトを生成する。
	"""
	
	if action == "post_add":
		#print(pk_set)
		solicitudes_pk_list = list(pk_set)
		added_pk = max(solicitudes_pk_list)

		if type(instance) != Item:
			return 
		item_obj = instance
		#print("TYPE")
		#print(type(item_obj))
		owner_user = Profile.objects.get(user=item_obj.user)
		#item_contact_objects = item_obj.item_contacts.all().order_by('timestamp')
		#item_contact_obj = item_contact_objects.last()

		aviso_user = owner_user
		Aviso.objects.create(
			aviso_user=aviso_user,
			content_type=ContentType.objects.get_for_model(item_obj.solicitudes.all().last()),
			object_id=added_pk)

		data = {"item_obj":item_obj.title }

		fcmd_obj = FireBaseMassagingDeal()
		fcmd_obj.getDeviceToken(aviso_user.user)
		fcmd_obj.makeNotification(case=FirebaseCloudMessagingCase.CREATED_SOLICITUD, data=data)
		fcmd_obj.makeMessage()
		fcmd_obj.sendMessage()

		
		# emailを送信するロジックを挿入
		subject = "ShareXekla Solicitud de transacción"
		content = item_obj.title + "\n" 
		message_to = [aviso_user.user.email]
		sendMail(subject, content, message_to)	


		

m2m_changed.connect(itemsolicitudes_m2m_changed_receiver, sender=Item.solicitudes.through)





def solicitud_post_save_receiver(sender, instance,created, *args, **kwargs):
	"""機能
	Solicitudインスタンスが変更されたときにインスタンスのacceptedがTrueかどうかチェックする。
	Trueの場合には他にもDirectMessageオブジェクトを作成するロジックを追加する。

	残念ながらsolicitud.acceptedをTrueに変えたときには最初にDirectMessageが生成され、その後Item.direct_messageに
	紐付けられるので現状firebaseのfcmを送信する事ができない。Itemオブジェクト変更後に発火するシグナルを準備する。
	"""
	
	
	#solicitudオブジェクトの変更があったときに以下のロジックに従ってDirectMessageオブジェクトが生成される
	if created == True:
		return
	solicitud_obj = instance

	item_obj = solicitud_obj.item_set.all().first()

	if item_obj == None:
		return

	if solicitud_obj.accepted == True and item_obj.direct_message is None:
		owner          = Profile.objects.get(user=item_obj.user)
		participant    = solicitud_obj.applicant
		dm_obj = DirectMessage.objects.create(
			owner       = owner, 
			participant = participant,
			)

		item_obj.direct_message = dm_obj
		item_obj._aviso_user = participant
		item_obj.save(update_fields=["direct_message"])
		#deadlineをTrueに変更する
		item_obj.deadline = True
		item_obj.save()
		return
	else:
		#print("不発です")
		return


post_save.connect(solicitud_post_save_receiver, sender=Solicitud )




def directmessage_post_save_receiver(sender, instance, created, *args, **kwargs):
	"""
	上記のsolicitud_post_save_receiverでDirectMessageオブジェクトが作成される。
	それをトリガーにavisoオブジェクトを生成する。

	"""
	if created == False:
		return



	dm_obj = instance
	aviso_user = dm_obj.participant


	aviso_obj = Aviso.objects.create(
		aviso_user=aviso_user, 
		content_type=ContentType.objects.get_for_model(dm_obj),   
		object_id=dm_obj.id,
		)

	#aviso_obj.aviso_user.add(aviso_user)

	try:
		item_obj = Item.objects.get(direct_message__id=dm_obj.id)

		
			
		#item_obj = dm_obj.item_set.all().first()
		data = {"item_obj":item_obj.title }
		fcmd_obj = FireBaseMassagingDeal()
		fcmd_obj.getDeviceToken(aviso_user.user)
		#fcmd_obj.makeNotification(case=FirebaseCloudMessagingCase.CREATED_DIRECTMESSAGE)
		fcmd_obj.makeNotification(case=FirebaseCloudMessagingCase.CREATED_DIRECTMESSAGE, data=data)
		fcmd_obj.makeMessage()
		fcmd_obj.sendMessage()
		
		#emailの送信を実装
		subject = "ShareXekla Ha sido elegido para hacer negocios con usted"
		content = item_obj.title + "\n" 
		message_to = [aviso_user.user.email]
		sendMail(subject, content, message_to)
		
	except:
		#sub_item_post_save_receiver()を使ってfcmとemailを送信する
		pass

	
post_save.connect(directmessage_post_save_receiver, sender=DirectMessage )







def sub_item_post_save_receiver(sender, instance, created, update_fields, *args, **kwargs):
	"""テスト実行
	
	"""

	if created == True:
		return


	#update_fieldsにdirect_messageがある場合にはfcm及びemailを送信する
	#update_fieldsを設定する場所はitemオブジェクトにdm_objを設定する場所、つまりこのファイルのsolicitud_post_save_receiverで実行する。
	if update_fields == None:
		return

	if "direct_message" in update_fields:

		item_obj = instance
		aviso_user = getattr(instance, '_aviso_user', None) #participantに該当する

		data = {"item_obj":item_obj.title }
		fcmd_obj = FireBaseMassagingDeal()
		fcmd_obj.getDeviceToken(aviso_user.user)
		#fcmd_obj.makeNotification(case=FirebaseCloudMessagingCase.CREATED_DIRECTMESSAGE)
		fcmd_obj.makeNotification(case=FirebaseCloudMessagingCase.CREATED_DIRECTMESSAGE, data=data)
		fcmd_obj.makeMessage()
		fcmd_obj.sendMessage()	
		
		#emailの送信
		subject = "ShareXekla Ha sido elegido para hacer negocios con usted"
		content = item_obj.title + "\n" 
		message_to = [aviso_user.user.email]
		sendMail(subject, content, message_to)		


post_save.connect(sub_item_post_save_receiver, sender=Item )







def dm_content_m2m_receiver(sender, instance, action, pk_set, *args, **kwargs):
	"""
	ダイレクトメッセージの送り主がメッセージを送信するたびに
	dm_objにdm_contentがaddされる。これをトリガーとしてAvisoオブジェクトが生成する。

	aviso_user = 通知を送る相手
	"""	
	if action == "post_add":
		dm_obj = instance
		#dm_content_objects = dm_obj.direct_message_contents.all()
		dm_content_objects_pk_set = list(pk_set)
		added_pk = max(dm_content_objects_pk_set)
		dm_content_obj = DirectMessageContent.objects.get(id=added_pk)


		if dm_obj.owner != dm_content_obj.profile:
			aviso_user = dm_obj.owner
		else:
			aviso_user = dm_obj.participant
	

		aviso_obj = Aviso.objects.create(
			aviso_user = aviso_user, 
			content_type=ContentType.objects.get_for_model(dm_content_obj),   
			object_id=dm_content_obj.id,
			)


		item_obj = Item.objects.get(direct_message=dm_obj)
		data = {"item_obj":item_obj.title }	


		fcmd_obj = FireBaseMassagingDeal()
		fcmd_obj.getDeviceToken(aviso_user.user)
		#fcmd_obj.makeNotification(case=FirebaseCloudMessagingCase.CREATED_DM_CONTENT)
		fcmd_obj.makeNotification(case=FirebaseCloudMessagingCase.CREATED_DM_CONTENT, data=data)
		fcmd_obj.makeMessage()
		fcmd_obj.sendMessage()

		#emailの送信を実装
		subject = "ShareXekla Tiene un mensaje"
		content = item_obj.title + "\n" 
		message_to = [aviso_user.user.email]
		sendMail(subject, content, message_to)			


m2m_changed.connect(itemsolicitudes_m2m_changed_receiver, sender=DirectMessage.direct_message_contents.through)





def user_post_save_receiver(sender, instance, created, *args, **kwargs):
	"""
	userオブジェクトが生成されたら自動的にProfileオブジェクトを生成する仕組み
	"""
	if created == False:
		return 
	elif created == True:
		user_obj = instance
		adm0 = "Guatemala"
		adm1 = "Quetzaltenango"
		adm2 = "Quetzaltenango"
		Profile.objects.create(user=user_obj, adm0=adm0, adm1=adm1, adm2=adm2)
		DeviceToken.objects.create(user=user_obj)
		return 


post_save.connect(user_post_save_receiver, sender=User)






def change_adm1_and_adm2_by_point_of_profile_obj(sender, instance, created, update_fields, *args, **kwargs):
	"""機能
	Profileオブジェクトのpoint属性が変更された時呼び出される。point値に基づいて
	DepartamentoやMunicipioの値を変更する


	"""
	if created == True:
		return 
	if update_fields == None:
		return
	if "point" in update_fields:
		print("pointをもとにadm1,adm2を修正")
		profile_obj = instance
		point = profile_obj.point
		departament_obj = Departamento.objects.get(adm1_es=profile_obj.adm1).geom
		print(departament_obj.contains(point))
		#含まれている時 -> 何もしない

		#含まれていない時 -> オブジェクトを変更する
		if departament_obj.contains(point) == False:
			print("pointをもとにadm1を修正")
			for dep in Departamento.objects.all():
				if dep.geom.contains(point):
					profile_obj.adm1 = dep.adm1_es
					profile_obj.save()

		#Municipioオブジェクトの取得
		muni_obj = Municipio.objects.get(adm2_es=profile_obj.adm2).geom

		#含まれていない時 -> オブジェクトを変更する
		if muni_obj.contains(point) == False:
			print("pointをもとにadm2を修正")
			rc_obj = RegionClassed.objects.get(departamento__adm1_es=profile_obj.adm1)
			for muni in rc_obj.municipios.all():
				if muni.geom.contains(point):
					profile_obj.adm2 = muni.adm2_es
					profile_obj.save()
		return

	#変更できなかった場合には通知を送信する仕組みを実装する(後で)

post_save.connect(change_adm1_and_adm2_by_point_of_profile_obj, sender=Profile)



