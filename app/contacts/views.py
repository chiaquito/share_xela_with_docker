from django.shortcuts import render, redirect
from django.views.generic import View
# Create your views here.
from .forms import ContactModelForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages

from .strings import emailSubject, content, sender, strMessage



from api.firebase_cloud_messaging import FireBaseMassagingDeal


class ContactView(View):
	"""
	非会員でもメッセージを送れる仕組みに変更する

	"""


	def get(self, request, *args, **kwargs):
		"""機能

		endpoint:
		name:
		"""

		context = {}	
		form = ContactModelForm()
		context["form"] = form
		return render(request, "contacts/contact.html", context)


	def post(self, request, *args, **kwargs):
		"""機能
		
		endpoint:
		name:
		"""		
		context = {}
		form = ContactModelForm(request.POST)
		if form.is_valid():
			form.save()
			#print(dir(form))
			#print(form.cleaned_data)
			clientEmailAddress = form.cleaned_data["email_address"]

			send_mail(
				emailSubject,
				content,
				sender,
				[clientEmailAddress,],
				)
			
			messages.info(self.request, strMessage)

			return redirect('home')
		else:
			#print("FORM IS INVALID")
			context["form"] = form
			return render(request, "contacts/contact.html", context)

