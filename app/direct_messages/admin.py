from django.contrib import admin
from .models import DirectMessage, DirectMessageContent
# Register your models here.


admin.site.register(DirectMessage)
admin.site.register(DirectMessageContent)