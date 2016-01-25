
from random import randint
import json
import simplejson
from datetime import datetime

from django.core import serializers
from django import http
from django.db import IntegrityError, transaction
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie.authentication import SessionAuthentication
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.http import HttpUnauthorized

from app.utils.balance_check import *
from app.utils.send_mail import *
#from app.forms import *
from app.models import * 


class UserResource(ModelResource):
        
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get','post']
        filtering = { "id" : ALL }

        fields = ['username', 'first_name', 'last_name', 'last_login']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('user_login'), name="api_login"),
            url(r"^(?P<resource_name>%s)/change_password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('change_password'), name="api_change_password"),
            url(r"^(?P<resource_name>%s)/update_password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_password'), name="api_update_password"),
            url(r"^(?P<resource_name>%s)/forgot_password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('forgot_password'), name="api_forgot_password"),
            url(r"^(?P<resource_name>%s)/new%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('new_user'), name="api_new_user"),
            url(r"^(?P<resource_name>%s)/update%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_user'), name="api_update_user"),
            url(r"^(?P<resource_name>%s)/edit%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('edit_user'), name="api_edit_user"),
            url(r"^user/logout/$", self.wrap_view('logout'), name='api_logout'),
            url(r"^(?P<resource_name>%s)/view%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_cards'), name="api_get_cards"),
            url(r"^(?P<resource_name>%s)/add_cards%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('add_cards'), name="add_cards"),
            url(r"^(?P<resource_name>%s)/balance%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('balance'), name="add_cards"),
   
        ]

    
    def add_cards(self, request, **kwargs):
        try:
            if not request.user.username:
                res = {"result": {"status": "False", "message": "User must login "}}
                return self.create_response(request, res)
            if request.method.lower() == 'post':
                input_data = json.loads(request.body)
                if [str(x) for x  in input_data.keys() if x not in ['name', 'number', 'retailer', 'pin']]:
                    res = {"result": {"status": "False", "message": "Input parameters are not correct"}}
                    return self.create_response(request, res)

                name = input_data.get("name", "")
                number = input_data.get("number", "")
                retailer_name = input_data.get("retailer", "")
                pin = input_data.get("pin", "")
                
                #user = User.objects.filter(username=request.POST["user"]).first()
                retailer = Retailer.objects.filter(name=retailer_name).first()
                #request.user = user;
                if input_data.get("expiration_date", ""):
                    from time import mktime, strptime
                    exp_date = datetime.strptime(request.get("expiration_date"), "%Y-%m-%d")
                else:
                    exp_date = ''
                wallet_objs = WalletCard.objects.filter(user=request.user)
                if wallet_objs:
                    for obj in wallet_objs:
                        if obj.card.number==number and obj.card.card_profile.retailer.name==retailer_name:
                            print number
                            res = {"result": {"status": "False", "message": "Card Already exist"}}
                            return self.create_response(request, res)

                #expiration_date = dateutil.parser.parse(request.POST["expiration_date"])
                expiration_date = exp_date
                cp = CardProfile()
                cp.retailer = retailer 
                cp.name = name
                cp.save()
                if cp:
                    add_card_obj = Card.objects.filter(
                        card_profile=cp,
                        number=number,
                        pin=pin)
                    if not add_card_obj:
                        add_card_obj, cre_card = Card.objects.get_or_create(
                            card_profile=cp,
                            number=number,
                            pin=pin)
                        if exp_date:
                            add_card_obj.expiration_date = exp_date
                            add_card_obj.save()

                    if add_card_obj:
                        card_details = {"number": number, "pin": pin, "type": retailer_name}
                        if input_data.get("balance", ""):
                            bal = input_data.get("balance")
                        else:
                            bal = 0
                            #bal_obj = BalanceCheck()
                            #bal = bal_obj.card_balance(card_details)
                        card_b = CardBalance()
                        card_b.card = add_card_obj
                        card_b.balance = bal
                        card_b.save()

                    if add_card_obj and request.user:
                        wallet_card = WalletCard.objects.filter(card=add_card_obj, user=request.user)
                        if not wallet_card:
                            wallet_obj, wall = WalletCard.objects.get_or_create(card=add_card_obj, user=request.user)
                            res = {"result": {"status": "True", "message": "Card Entered Success"}}
                        else:
                            res = {"result": {"status": "True", "message": "Card Already mapped"}}
            else:
                res = {"result": {"status": "False", "message": "Method Not allowed"}}
   
        except:
            res = {"result": {"status": "False", "message": "User Not allowed"}}
        return self.create_response(request, res)

    @csrf_exempt
    def new_user(self, request, **kwargs):
        try:
            if request.method.lower() in ['post']:
                input_data = json.loads(request.body)
                username = input_data.get('username', "")
                password = input_data.get("password", "")
                isactive = False
                email = ""
                mobile = ""
                if username:
                    if '@' in username:
                        email = username
                        user = User.objects.filter(email=email)
                    else:
                        mobile = username
                        user = UserProfile.objects.filter(mobile=username)
                    if user:
                        res = {"result": {"status": "False", "message": "Username already exist"}}
                    else:
                        user_obj, new_user = User.objects.get_or_create(username=username, email=email,is_active=isactive)
                        user_obj.set_password(password)
                        user_obj.save()
                        if user_obj:
                            otp_random = randint(0,999999)
                            otp_create, otp_true = OneTimePassword.objects.get_or_create(user=user_obj, otp=otp_random)
                            try:
                                up_obj, up = UserProfile.objects.get_or_create(user=user_obj, mobile=mobile)
                                up_obj.save()
                            except:
                                pass
                            if user_obj.email:
                                send_mail2(user_obj.email, "OTP", "your OTP is : "+str(otp_random))
                            if mobile:
                                send_sms=send_sms_msg91(mobile, "your OTP is : "+str(otp_random))
                                if send_sms:
                                    res = {"result": {"status": "True", "otp_data":otp_random}}
                                else:
                                    res = {"result": {"status": "True", "message": "SMS Not send", "otp_data": otp_create.otp}}
                else:
                    res = {"result": {"status": "False", "message": "Username data is empty"}}

            else:
                res = {"result": {"status": "False", "message": "Method Not allowed"}}
        except:
            res = {"result": {"status": "False", "message": "Something went Wrong "}}
        return self.create_response(request, res)

    @csrf_exempt
    def user_login(self, request, **kwargs):
        try:
            if request.method.lower() == 'post':
                # if request.POST.get('facebook'):
                #     self.fb_login(request)
                input_data = json.loads(request.body)
                username = input_data.get('username', "")
                password = input_data.get("password", "")
                user_check = User.objects.filter(username=username)
                if user_check:
                    username = user_check[0].username
                else:
                    up_obj = UserProfile.objects.filter(mobile=username)
                    if up_obj:
                        username = up_obj[0].user.username
                    else:
                        username = ''

                if username and password:
                    user = authenticate(username=username, password=password)
                    if user:

                        #user = User.objects.filter(username=username, password=password)
                        if user.is_active:
                            login(request, user)
                            user.is_authenticated()
                            user_result = {}
                            user_result['username'] = user.username
                            user_result['first_name'] = user.first_name
                            user_result['last_name'] = user.last_name
                            user_pro= UserProfile.objects.filter(user=user)
                            if user_pro:
                                user_pro = user_pro[0]
                                user_result['user_image'] = str(user_pro.user_image.url)
                            res = {"result": {"status": "True", "user": user_result, "message": "Login success"}}
                        else:
                            otp_random = randint(0,999999)
                            otp_create, otp_true = OneTimePassword.objects.get_or_create(user=user, otp=otp_random)
                            if user.email:
                                send_mail2(user.email, "OTP", "your OTP is : "+str(otp_random))
                            res = {"result": {"status": "False", "message": "Your account is not verified yet", "otp": otp_create.otp}}
                    else:
                        res = {"result": {"status": "False", "message": "Username or password is not correct"}}
                else:
                    res = {"result": {"status": "False", "message": "Username / password is not available"}}
            else:
                res = {"result": {"status": "False", "message": "Method Not allowed"}}
        except:
            res = {"result": {"status": "False", "message": "Something went Wrong "}}
        return self.create_response(request, res)

    def fb_login(self, request):

        try:
            return True

        except:
            res = {"result": {"status": "False", "message": "Something went Wrong "}}
        return HttpResponse(simplejson.dumps(res), content_type="application/json")


    def change_password(self, request, **kwargs):
        try:
            if request.method.lower() == 'post':
                username = request.user.username
                input_data = json.loads(request.body)
                #username = request.user.username
                old_password = input_data.get("old_password", "")
                change_type = input_data.get("change_type", "")
                new_password = input_data.get("new_password", "")
                user_obj = ''
                if not old_password or not new_password:
                    res = {"result": {"status": "False", "message": "New or Old Password is empty "}}
                    return self.create_response(request, res, HttpResponse)
                if old_password:
                    user_obj = authenticate(username=username, password=old_password)
                if user_obj and new_password:
                    user_obj.set_password(new_password)
                    user_obj.save()
                    login(request, user_obj)
                    user_obj.is_authenticated()

                    res = {"result": {"status": "True", "message": "Password Changed successfully"}}
                else:
                    res = {"result": {"status": "False", "message": "User Does not exist"}}
            else:
                res = {"result": {"status": "False", "message": "Method Not allowed"}}
        except:
            res = {"result": {"status": "False", "message": "Something went Wrong "}}
        return self.create_response(request, res, HttpResponse)

    @csrf_exempt
    def update_password(self, request, **kwargs):
        try:
            if request.method.lower() == 'post':
                input_data = json.loads(request.body)
                change_type = input_data.get("change_type", "")
                new_password = input_data.get("new_password", "")
                user_obj = ''
                username = input_data.get("username", "")
                if username and change_type == 'FORGOT':
                    user_obj = User.objects.get(username=username)
                    if user_obj and new_password:
                        user_obj.set_password(new_password)
                        user_obj.save()
                        res = {"result": {"status": "True", "message": "Password Updated successfully"}}
                else:
                    res = {"result": {"status": "False", "message": "User Does not exist"}}
            else:
                res = {"result": {"status": "False", "message": "Method Not allowed"}}
        except:
            res = {"result": {"status": "False", "message": "Something went Wrong "}}
        return self.create_response(request, res, HttpResponse)

    @csrf_exempt
    def forgot_password(self, request, **kwargs):
        try:
            if request.method.lower() == 'post':
                input_data = json.loads(request.body)
                username = input_data.get("username", "")
                if '@' in username:
                    email = username
                    user = User.objects.filter(email=email)
                #         raise CustomBadRequest(
                #             code="duplicate_exception",
                #             message="That email is already used.")
                if username:
                    user_obj = User.objects.get(username=username)
                    if user_obj:
                        otp_random = randint(0,999999)
                        otp_create, otp_true = OneTimePassword.objects.get_or_create(
                            user=user_obj, otp=otp_random, otp_types = 'FORGOT')
                        if user_obj.email:
                            send_mail2(user_obj.email, "OTP", "Password Reset OTP is : "+str(otp_random))
                        #up_create, upp_true = UserProfile.objects.get_or_create(user=user_obj)
                        res = {"result": {"status": "True", "otp_data": otp_create.otp}}
                    else:
                        res = {"result": {"status": "False", "message": "User Does not exist"}}
            else:
                res = {"result": {"status": "False", "message": "Method Not allowed"}}
        except:
            res = {"result": {"status": "False", "message": "Something went Wrong "}}
        return self.create_response(request, res)

    def edit_user(self, request, **kwargs):
        try:
            if request.user.username:
                user_pro= UserProfile.objects.filter(user=request.user)[0]
                user_result = {} 
                user_result['username'] = request.user.username
                user_result['first_name'] = request.user.first_name
                user_result['last_name'] = request.user.last_name
                user_result['email'] = request.user.email
                user_result['mobile'] = user_pro.mobile
                res = {"result": {"status": "True", "data": user_result, "message": "success"}}
            else:
                res = {"result": {"status": "False", "message": "User does not exist"}}
   
        except:
            res = {"result": {"status": "False", "message": "User Not allowed"}}
        return self.create_response(request, res)


    def update_user(self, request, **kwargs):
        try:
            if request.user.username:
                input_data = json.loads(request.body)
                user_pro= UserProfile.objects.filter(user=request.user)[0]
                if input_data.get('first_name', ''):
                    request.user.first_name = input_data['first_name']
                if input_data.get('last_name', ''):
                    request.user.last_name = input_data['last_name']
                request.user.save() 
                #user_pro.save()
                user_result = {} 
                user_result['username'] = request.user.username
                user_result['first_name'] = request.user.first_name
                user_result['last_name'] = request.user.last_name
                user_result['email'] = request.user.email
                user_result['mobile'] = user_pro.mobile
                res = {"result": {"status": "True", "data": user_result, "message": "success"}}
            else:
                logout(request.user)
                res = {"result": {"status": "False", "message": "User does not exist"}}
   
        except:
            res = {"result": {"status": "False", "message": "Not allowed"}}
        return self.create_response(request, res)

    def logout(self, request, **kwargs):
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)


    def get_cards(self, request, **kwargs):
        try:
            if not request.user.username:
                res = {"result": {"status": "False", "message": "User Not login"}}
                return self.create_response(request, res)
            else:
                cards = WalletCard.objects.filter(user=request.user)
                user_result = {}
                user_result['username'] = request.user.username
                user_result['first_name'] = request.user.first_name
                user_result['last_name'] = request.user.last_name
                card_list = []
                if cards:      
                    for wcard in cards:
                        card_values = {}
                        bal = CardBalance.objects.filter(card = wcard.card)[0]
                        card_values['card_id'] = wcard.card.id
                        card_values['number'] = wcard.card.number
                        card_values['pin'] = wcard.card.pin
                        card_values['profile_name'] = wcard.card.card_profile.name
                        card_values['retailer'] = wcard.card.card_profile.retailer.name
                        card_values['balance'] = bal.balance
                        card_values['logo'] = wcard.card.card_profile.retailer.logo
                        card_values['site_url'] = wcard.card.card_profile.retailer.site_url

                        card_list.append(card_values)

                    user_result['cards'] = card_list
                    res = {"result": {"status": "True", "data": user_result, "message": "success"}}
                else:
                    res = {"result": {"status": "True", "data": user_result, "message": "No Cards available"}}
        except:
            res = {"result": {"status": "False", "message": "Something went Wrong "}}
        return self.create_response(request, res)

    def balance(self, request, **kwargs):
        try:
            if not request.user.username:
                res = {"result": {"status": "False", "message": "User Not login"}}
                return self.create_response(request, res)
            if request.method.lower() == 'post':
                input_data = json.loads(request.body)
                card_id = input_data.get("card_id", "")
                balance = input_data.get("balance", "")
                bal_obj = ""
                if card_id and card_id.isdigit():
                    bal_obj = CardBalance.objects.filter(card_id=int(card_id))
                if bal_obj and WalletCard.objects.filter(user=request.user, card_id=int(card_id)):
                    bal_obj[0].balance = balance
                    bal_obj[0].save()
                    res = {"result": {"status": "True", "message": "Balance updated Success"}}
                else:
                    res = {"result": {"status": "False", "message": "Card Does not exist"}}
            else:
                    res = {"result": {"status": "False",  "message": "Method not allowed"}}
        except:
            res = {"result": {"status": "False", "message": "Something went Wrong "}}
        return self.create_response(request, res)

    

