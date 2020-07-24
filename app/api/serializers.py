from rest_framework import serializers
from django.contrib.auth.models import User
from avisos.models import Aviso
from categories.models import Category
from contacts.models import Contact
from direct_messages.models import DirectMessageContent
from direct_messages.models import DirectMessage
from feedback.models import Feedback
from item_contacts.models import ItemContact
from items.models import Item
from profiles.models import Profile
from solicitudes.models import Solicitud


"""
クラス命名規則

ModelSerializerを採用しているので、
Serializer名は、 "Appのクラス名 + Serializer" とする。

"""




class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model  = Category
		#fields = "__all__"
		fields = ("number",)



class ContactSerializer(serializers.ModelSerializer):

	class Meta:
		model = Contact
		fields = ("title", "email_address", "content",)



class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		#fields = "__all__"
		fields = ("id","username","email")



class FeedbackSerializer(serializers.ModelSerializer):
	evaluator = UserSerializer()
	class Meta:
		model = Feedback
		fields = ("id", "evaluator", "content", "level")





class ProfileSerializer(serializers.ModelSerializer):

	user     = UserSerializer()
	feedback = FeedbackSerializer(read_only=True, many=True)
	class Meta:
		model = Profile
		fields = ("user", "adm0", "adm1", "adm2", "description", "feedback", "point", "radius", "image", "sex") #"phonenumber", "birthday",



	
	def update(self, instance, validated_data):
		#ネストされているデータはシリアライザで更新する事ができない。
		#ネストされているユーザーオブジェクトだけ自分で更新し、ネストされているデータは削除する。


		print("validated_data: ",validated_data)
		user_obj_id = validated_data.pop("user_obj_id")
		print("USER_OBJ_ID", user_obj_id)
		user_obj = User.objects.get(id=user_obj_id)


		if "user" in validated_data.keys():
			user_data = validated_data.pop("user")
			print(user_data)

			
			#print(user_data.get("email", None))
			username = user_data.get("username", None)
			email = user_data.get("email", None)

			if username != None:
				user_obj.username = username

			if email != None:
				user_obj.email = email

			user_obj.save()	
		return super().update(instance, validated_data)





class ItemContactSerializer(serializers.ModelSerializer):

	post_user = ProfileSerializer(read_only=True)
	#item = ItemSerializer(read_only=True)
	#reply_user = ProfileSerializer(read_only=True) #今後はこのreply_userフィールドを削除する。未削除状態。


	class Meta:
		model = ItemContact
		#fields = "__all__"
		fields = ("post_user","message", "timestamp") # "item", 



	


class SolicitudSerializer(serializers.ModelSerializer):

	#item = ItemSerializer(read_only=True)#
	applicant = ProfileSerializer(read_only=True)

	class Meta:
		model = Solicitud
		fields = ("id", "applicant", "message", "timestamp", "accepted") # applicantは申請者(応募者を示す) ,"item", 




class DirectMessageContentSerializer(serializers.ModelSerializer):

	#dm = DirectMessageSerializer(read_only=True)
	profile = ProfileSerializer(read_only=True)

	class Meta:
		model = DirectMessageContent
		#fields = "__all__"
		fields = ('content', 'profile', 'created_at') #'dm', 
		read_only_fields = ('created_at',) #'dm', 'profile',



class DirectMessageSerializer(serializers.ModelSerializer):

	#item  = ItemSerializer()
	owner                   = ProfileSerializer()
	participant             = ProfileSerializer()
	direct_message_contents = DirectMessageContentSerializer(read_only=True, many=True)

	class Meta:
		model = DirectMessage
		fields = (
			'id', 'owner', 'participant', 'direct_message_contents',
			'is_feedbacked_by_owner', 'is_feedbacked_by_participant', 'created_at'
		) #'item', 




class ItemSerializer(serializers.ModelSerializer):
	#profile = ProfileSerializer()
	#user = UserSerializer()
	#user = serializers.StringRelatedField()
	#user = serializers.PrimaryKeyRelatedField(read_only=True)
	#itemcontact_set = ItemContactSerializer()_
	category       = CategorySerializer(read_only=True)
	user           = UserSerializer(read_only=True)
	favorite_users = UserSerializer(read_only=True, many=True)
	item_contacts  = ItemContactSerializer(read_only=True, many=True) #追加
	solicitudes    = SolicitudSerializer(read_only=True, many=True) #追加
	direct_message = DirectMessageSerializer(read_only=True) #追加



	class Meta:
		model = Item
		#fields = "__all__" "profile"
		fields = (
			"id", "title", "description", "category",
			"adm0", "adm1", "adm2", "point", "radius", 
			"created_at", "active","deadline","favorite_users",
			"item_contacts", "solicitudes", "direct_message",
			"image1", "image2", "image3", "user", "price"
			 ) 



#webで変更した項目
# MODEL: Item-済, DirectMessage-済, DirectMessageContent-済, Solicitud-済, ItemContact-済
# VIEW : 上記に含めてAviso

#apiで変更スべき点
# serializers.py
# serializers.pyに基づいてviews.pyを変更する

#スマホの変更点
#dataモデルの変更
#各ロジックの変更


	
	def create(self,  validated_data):

		#super().save(*args, **kwargs)
		#Itemオブジェクトの生成
		#item_obj = Item.objects.create(
		#	title = request.data["title"],
		#		description = request.data["description"],
		#	category = category_obj,
		#	adm0 = request.data["adm0"],
		#	adm1 = request.data["adm1"], 
		#	adm2 = request.data["adm2"]
		#	)


		Item.objects.create(**validated_data)

		print("Itemオブジェクトの生成")
		#return super(Item, self).create(*args, **kwargs)
	









class AvisoObjectRelatedField(serializers.RelatedField):


	def to_representation(self, value):
		#print("VALUEのチェックを実行する")
		#print(dir(value))
		#print(value.item)
		content_object = {}

		if isinstance(value, ItemContact):
			content_object["modelName"] = "ItemContact"
			#content_object["itemName"] = str(value.item)
			content_object["itemName"] = Item.objects.get(item_contacts__id=value.id).title#get(direct_message=value.id).title

		elif isinstance(value, Solicitud):
			content_object["modelName"] = "Solicitud"
			#content_object["itemName"] = str(value.item)
			content_object["itemName"] = Item.objects.get(solicitudes__id=value.id).title
		elif isinstance(value, DirectMessage):
			content_object["modelName"] = "DirectMessage"
			#content_object["itemName"] = str(value.item)
			print(value)
			print(dir(value))
			content_object["itemName"] = Item.objects.get(direct_message__id=value.id).title
			#content_object["itemName"] = Item.objects.filter(direct_message__id=value.id).first().title
		elif isinstance(value, DirectMessageContent):
			content_object["modelName"] = "DirectMessageContent"
			#content_object["sendUserName"] = str(value.profile)
			dm_obj = DirectMessage.objects.get(direct_messages__id=value.id)
			content_object["itemName"] = Item.objects.get(direct_message__id=dm_obj.id).title
		else:
			print("ちゅうううううううううい")
			print(value)
		return content_object






class AvisoSerializer(serializers.ModelSerializer):

	content_object = AvisoObjectRelatedField(read_only=True)
	aviso_user = ProfileSerializer()
	#aviso_user = ProfileSerializer(many=True)


	class Meta:
		model = Aviso
		fields = ('aviso_user', 'content_type', 'object_id', 'content_object',  'checked', 'created_at') #




