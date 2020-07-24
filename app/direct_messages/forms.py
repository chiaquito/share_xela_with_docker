from django import forms
from django.forms.models import ModelChoiceField
from .models import Profile
#from django.contrib.auth.models import User
from .models import DirectMessageContent
from .models import DirectMessage



class DirectMessageContentModelForm(forms.ModelForm):
	#dm      = ModelChoiceField(queryset=DirectMessage.objects.all())
	#profile = ModelChoiceField(queryset=Profile.objects.all())

	class Meta:
		model = DirectMessageContent
		fields = ("content", ) #"dm", "profile"


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():

			self.fields["content"].widget.attrs["class"] = "form-control col-auto"
			self.fields["content"].widget.attrs["rows"]  = "4"
			#self.fields["content"].widget.attrs["placeholder"]  = "取引の具体的な場所や日時をメッセージでやり取りしてください"
			self.fields["content"].widget.attrs["placeholder"]  = "Intercambie la fecha, hora y lugar específicos de la transacción en mensajes"
			



