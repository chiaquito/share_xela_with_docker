from django import forms
from .models import Item
#from .models import Prefectura

from categories.models import CATEGORY_CHOICE, Category






class ItemModelForm(forms.ModelForm):
	category = forms.ModelChoiceField(queryset=Category.objects.all())

	class Meta:
		model  = Item

		fields = ('category', 'title', 'price','description', 'adm0', 'image1','image2','image3',  ) #,'image4','image5','image6' "point", "radius" 'adm1', 'adm2',
		
		#fields = '__all__' 


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#for field in self.fields.values():
		#self.fields["user"].widget.attrs["class"] = "form-control"
		#self.fields["user"].required = False

		self.fields["category"].widget.attrs["class"] = "form-control"
		#self.fields["category"].widget.attrs["size"] = "7"
		#self.fields["category"].required = False


		self.fields["title"].widget.attrs["class"] = "form-control"
		self.fields["description"].widget.attrs["class"] = "form-control "#h-25rows="4"
		self.fields["description"].widget.attrs["rows"]  = "6"
		self.fields["title"].widget.attrs["size"] = "5"
		self.fields["price"].widget.attrs["class"] = "form-control"


		self.fields["adm0"].widget.attrs["class"] = "form-control"
		#self.fields["adm1"].widget.attrs["class"] = "form-control"
		#self.fields["adm2"].widget.attrs["class"] = "form-control"
		self.fields["image1"].widget.attrs["class"] = "form-control"
		self.fields["image1"].widget.attrs["type"] = "file"
		self.fields["image1"].widget.attrs["size"] = "8"
		self.fields["image2"].widget.attrs["class"] = "form-control"
		self.fields["image2"].widget.attrs["type"] = "file"
		self.fields["image3"].widget.attrs["class"] = "form-control"
		self.fields["image3"].widget.attrs["type"] = "file"
		#self.fields["image4"].widget.attrs["class"] = "form-control"
		#self.fields["image4"].widget.attrs["type"] = "file"
		#self.fields["image5"].widget.attrs["class"] = "form-control"
		#self.fields["image5"].widget.attrs["type"] = "file"
		#self.fields["image6"].widget.attrs["class"] = "form-control"
		#self.fields["image6"].widget.attrs["type"] = "file"

		#self.fields["category"].widget = forms.Select(choices=CATEGORY_CHOICE, attrs={'class': 'form-control'})





class ItemFirstModelForm(forms.ModelForm):
	class Meta:
		model  = Item
		fields = ('category', 'title', 'description', 'image1')





