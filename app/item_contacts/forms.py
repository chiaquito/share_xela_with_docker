from django import forms
from django.forms.models import ModelChoiceField
from django.contrib.auth.models import User
from item_contacts.models import ItemContact
from profiles.models import Profile





#class CustomModelChoiceField()




class ItemContactModelForm(forms.ModelForm):

	#reply_user = ModelChoiceField(queryset=Profile.objects.all())
	
	class Meta:
		model  = ItemContact
		fields = (  'message',  ) #'reply_user' 'item', 'post_user',




	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#for field in self.fields.values():
		#	#self.fields["reply_to"].widget.attrs["class"] = "form-control"
		#	#self.fields["message"].widget.attrs["class"] = "form-control form-control-sm"
		self.fields["message"].widget.attrs["class"] = "form-control"
		self.fields["message"].widget.attrs["rows"] = "5"

