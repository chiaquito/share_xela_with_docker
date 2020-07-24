from django import forms
from .models import Contact


class ContactModelForm(forms.ModelForm):

	class Meta:
		model  = Contact
		fields = ("title", "email_address", "content")


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#self.fields["user"].widget.attrs["class"] = "form-control"
		self.fields["title"].widget.attrs["class"] = "form-control"
		self.fields["email_address"].widget.attrs["class"] = "form-control"
		self.fields["content"].widget.attrs["class"] = "form-control"
		self.fields["content"].widget.attrs["rows"] = "7"
