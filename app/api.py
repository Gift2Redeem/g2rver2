from tastypie.resources import ModelResource, Resource
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.models import ApiKey
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from app.balance_check.card_balance import *
from app.models.card_details import *
from django.http import Http404
from django.http import HttpResponse
import simplejson
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.core import serializers
from decimal import *
from datetime import datetime
import dateutil.parser
import simplejson
import time
import smtplib
import string
import socket


def otp_email(req):
        gmail_user = "michaleraj2008@gmail.com"
        gmail_pwd = "poogaymic!@#2014"
        TO = 'michaleraj2008@gmail.com'
        SUBJECT = "G2R OTP Verification"
        TEXT = "Hi Michale Raj,\n\nYour one time password for g2r is :854678\n\nRegards,\nG2R Team."
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        BODY = '\r\n'.join(['To: %s' % TO,
                'From: %s' % gmail_user,
                'Subject: %s' % SUBJECT,
                '', TEXT])

        server.sendmail(gmail_user, [TO], BODY)
        return HttpResponse("Email Sent")

def validate_user(req):
	#import pdb;pdb.set_trace()
	if req.method=="POST":
		firstName=req.POST["first_name"]
		lastName=req.POST["last_name"]
		username = req.POST["username"]
		logmethod=req.POST["login_method"]
		password = req.POST["password"]
		user = User.objects.filter(username=username)
		if not user:
                    return HttpResponse("Not registered", content_type="application/json")

		if logmethod =='':
			user = authenticate(username=username, password=password)
		else:
			emailId=username
			retailers = serializers.serialize("json", Retailer.objects.all())
			cards = serializers.serialize("json", Card.objects.all())
			cardbalance = serializers.serialize("json", CardBalance.objects.all())
			data = {'data': {'profile': {'username' : username, 'firstName' : firstName, 'lastName' : lastName, 'email' : emailId}, 'retailers': retailers, 'cards': cards, 'cardbalance':cardbalance,'session_id' : 'fkjsfh34' }}
			return HttpResponse(simplejson.dumps(data), content_type="application/json")

		if user is not None:
			if user.is_active:
				login(req, user)
				user = User.objects.get(username=username)
				username = user.username
				firstName = user.first_name
				lastName = user.last_name
				emailId = user.email
				retailers = serializers.serialize("json", Retailer.objects.all())
				cards = serializers.serialize("json", Card.objects.all())
				data = {'data': {'profile': {'username' : username, 'firstName' : firstName, 'lastName' : lastName, 'email' : emailId}, 'retailers': retailers, 'cards': cards, 'session_id' : 'fkjsfh34' }}
				print (data)
				return HttpResponse(simplejson.dumps(data), content_type="application/json")
			else:
				return HttpResponse("User is currently not active! Please contact support.")
		else:
			return HttpResponse("Username/password combination is invalid! Try again")
	else:
		return HttpResponse("Http Method Not Supported")


def get_user_data(req):
	if req.method == "POST":
		userId = req.POST["userId"]
		retailers = serializers.serialize("json", Retailer.objects.all())
		cards = serializers.serialize("json", RetailerCard.objects.all())
		data = {'data': {'profile': {}, 'retailers': retailers, 'cards': cards, 'session_id' : 'fkjsfh34' }}
		print (data)
		return HttpResponse(simplejson.dumps(data), content_type="application/json")
	else:
		return HttpResponse("Username/password combination is invalid! Try again")



def register_user(req):
	if req.method == "POST":
		username = req.POST["mobileNumber"]
		emailId = req.POST["email"]
		password = req.POST["password"]
		firstName = req.POST["firstName"]
		lastName = req.POST["lastName"]
		try:
			user = User.objects.get(username=username)
			return HttpResponse("User already exists");
		except User.DoesNotExist:
			user = User.objects.create_user(username, emailId, password)
			user.first_name = firstName
			user.last_name = lastName
			user.save()
			retailers = serializers.serialize("json", Retailer.objects.all())
			cards = serializers.serialize("json", RetailerCard.objects.all())
			data = {'data' : {'profile':{'username' : username, 'firstName' : firstName, 'lastName' : lastName, 'email' : emailId}, 'retailers' : retailers, 'cards': cards, 'session_id' : 'hgjdwds'}}
			
			return HttpResponse(simplejson.dumps(data), content_type="application/json")

#######################################################################################################
#######################################################################################################
## Basic Flow
## Create Account -> Add Card(s) -> View Offers and Retailer Balances
#######################################################################################################
#######################################################################################################

#######################################################################################################
# Create a new gift2redeem account by provisioning a username and API key
# POST -> /api/v1/account/
#######################################################################################################

def create_new_account(req):
	if req.method == "POST":
		user_name = req.POST["username"]
		resp = User.objects.get_or_create("dd","dd","dd")
		print (resp)
		user = resp[0]
		resp = ApiKey.objects.get_or_create(user=user.id)
		api_key = resp[0]
		api_key.key = api_key.generate_key()
		api_key.save()
		data = {"username" : user_name, "api_key" : api_key.key}
		print (data)
		return HttpResponse(simplejson.dumps(data), content_type="application/json")
	else:
		return HttpResponse(status=404)



