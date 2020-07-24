from django.shortcuts import render, redirect
from django.views.generic import View
# Create your views here.

from favorite.models import Favorite
from django.contrib.auth.models import User



class FavoriteView(View):

    def get(self, request, *args, **kwargs):

        if request.user.is_anonymous:
            return redirect(ViewName.HOME)

        request_user_obj = User.objects.get(username=request.user.username)
        fav_objects = Favorite.objects.filter(user=request_user_obj)
        


