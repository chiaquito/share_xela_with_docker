from django import forms

from .models import Profile
from tempus_dominus.widgets import DatePicker



class ProfileForm(forms.ModelForm):


	class Meta:
		model  = Profile
		fields = ('user','adm0', 'adm1', 'adm2', 'birthday', 'image', 'phonenumber', 'description') #


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#for field in self.fields.values():
		self.fields["birthday"].widget = DatePicker()

		self.fields["adm0"].widget.attrs["class"] = "form-control mt-2 select_height"
		#self.fields["adm1"].widget.attrs["class"] = "form-control"
		#self.fields["adm2"].widget.attrs["class"] = "form-control"
		self.fields["image"].widget.attrs["class"] = "form-control"
		#self.fields["image"].widget.attrs["@change"] = "onFileChange"
		self.fields["phonenumber"].widget.attrs["class"] = "form-control"
		self.fields["phonenumber"].widget.attrs["placeholder"] = "reparar cuando tengo tiempo"
		self.fields["user"].widget.attrs["class"] = "form-control"
		self.fields["user"].widget.attrs["disabled"] = "disabled"
		self.fields["description"].widget.attrs["class"] = "form-control"
		self.fields["description"].widget.attrs["rows"] = "9"



			#<input type="text" name="test" class="form-control-plaintext" readonly="False" value="testy">


			

class CreatingProfileForm(forms.ModelForm):

	class Meta:
		model  = Profile
		fields = ('user','adm0', 'adm1', 'adm2',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["adm0"].widget.attrs["class"] = "form-control"
		self.fields["adm1"].widget.attrs["class"] = "form-control"
		self.fields["adm2"].widget.attrs["class"] = "form-control"






