from allauth.account.forms import LoginForm, SignupForm, _base_signup_form_class
from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UsernameField, UserChangeForm
from django.contrib.auth.validators import UnicodeUsernameValidator

from allauth.account import app_settings




#########################################
## django-allauthのformクラスのカスタム  ##
#########################################

#allauthのLoginFormのカスタム
# https://django-allauth.readthedocs.io/en/latest/forms.html#login-allauth-account-forms-loginform
class MyCustomLoginForm(LoginForm):

    def login(self, *args, **kwargs):

        # Add your own processing here.

        # You must return the original result.
        return super(MyCustomLoginForm, self).login(*args, **kwargs)


    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	for field in self.fields.values():
    		field.widget.attrs['class'] = "form-control"
    		#field.widget.attrs['placeholder'] = field.label




#allauthのSignupFormのカスタム
# https://django-allauth.readthedocs.io/en/latest/forms.html#signup-allauth-account-forms-signupform
class MyCustomSignupForm(SignupForm):

	def save(self, request):

		# Ensure you call the parent class's save.
		# .save() returns a User object.
		user = super(MyCustomSignupForm, self).save(request)

		# Add your own processing here.

		# You must return the original result.
		return user

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = "form-control"
	









##################################################
###   profileページ上のuserデータ変更のフォーム    ###
##################################################

class UsernameChangeForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ("username",)
		field_classes = {'username': UsernameField}


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["username"].widget.attrs["class"] = "form-control"
		self.fields["username"].widget.attrs['placeholder'] = "150 characters or fewer. Letters, digits and @/./+/-/_ only."

	#個別フィールドのバリデーションチェック
	#def clean_username(self):
	#	username = self.cleaned_data['username']
	#	if len (username) < 3:
	#		raise forms.ValidationError("n駄目です")
	#	return username


class EmailAddressChangeForm(forms.ModelForm):

	class Meta:
		model  = User
		fields = ("email",)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["email"].widget.attrs["class"] = "form-control"




