from django.shortcuts import render
from django import http
from django.db import IntegrityError, transaction
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url
from django.contrib.auth.models import User
from tastypie.http import HttpResponse
import json

# Create your views here.
def user_login(request):
    try:
        import pdb; pdb.set_trace()
        if request.method == 'POST':
       
            username = request.POST["username"]
            
            if username:
                msg="Login success"
                #login(request, user)
                success = True
                #next_url = reverse('events:new')
            else:
                msg = "Invalid Username or Password"
                success = False

            return HttpResponse({'msg' : msg, 'success' : success})

    except:
        raise HttpResponse(
            message="Porblem in user login.")