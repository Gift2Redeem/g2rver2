
from random import randint
import simplejson
from django.core import serializers
from django import http
from django.db import IntegrityError, transaction
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse

from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.http import HttpUnauthorized

from app.utils.balance_check import *
#from app.forms import *
from app.models import *
from datetime import datetime


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get','post']
        filtering = { "id" : ALL }

        fields = ['username', 'first_name', 'last_name', 'last_login']

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('user_login'), name="api_login"),
            url(r"^(?P<resource_name>%s)/change_password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('change_password'), name="api_change_password"),
            url(r"^(?P<resource_name>%s)/new%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('new_user'), name="api_new_user"),
            url(r"^user/logout/$", self.wrap_view('logout'), name='api_logout'),
            url(r"^(?P<resource_name>%s)/view%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_cards'), name="api_get_cards"),
            url(r"^(?P<resource_name>%s)/add_cards%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('add_cards'), name="add_cards"),
            url(r"^(?P<resource_name>%s)/offers%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('offers'), name="offers"),
            url(r"^(?P<resource_name>%s)/new_card%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('new_card'), name="api_new_card"),


        ]


    def add_cards(self, request, **kwargs):

        try:
            if not request.user:
                res = {"result": {"status": "False", "message": "User Not allowed"}}
                return HttpResponse(simplejson.dumps(res), content_type="application/json")
            if request.method.lower() == 'post':

                # username = request.POST['username']
                # user_obj = User.objects.filter(username=username).first()
                name = request.POST["name"]
                number = request.POST["number"]
                retailer_name = request.POST["retailer"]
                #user = User.objects.filter(username=request.POST["user"]).first()
                retailer = Retailer.objects.filter(name=request.POST["retailer"]).first()
                #request.user = user;
                pin = request.POST["pin"]
                if request.POST.get("expiration_date"):
                    from time import mktime, strptime
                    exp_date = datetime.strptime(request.POST["expiration_date"], "%Y-%m-%d")
                else:
                    exp_date = ''

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
                            pin=pin,
                            expiration_date=expiration_date)
                    if add_card_obj:
                        card_details = {"number": number, "pin": pin, "type": retailer_name}
                        if request.POST.get("balance"):
                            bal = request.POST["balance"]
                        else:
                            bal_obj = BalanceCheck()
                            bal = bal_obj.card_balance(card_details)
                        card_b = CardBalance()
                        card_b.card = add_card_obj
                        card_b.balance = bal
                        card_b.save()

                    if add_card_obj and request.user:
                        wallet_card = WalletCard.objects.filter(card=add_card_obj, user=request.user)
                        if not wallet_card:
                            wallet_obj, wall = WalletCard.objects.get_or_create(card=add_card_obj, user=request.user)
                            res = {"result": {"status": "True", "message": "Card Entered Success"}}
                            return HttpResponse(simplejson.dumps(res), content_type="application/json")
                        else:
                            res = {"result": {"status": "True", "message": "Card Already mapped"}}
                            return HttpResponse(simplejson.dumps(res), content_type="application/json")
            else:
                res = {"result": {"status": "False", "message": "User Not allowed"}}
                return HttpResponse(simplejson.dumps(res), content_type="application/json")

        except:
            res = {"result": {"status": "False", "message": "User Not allowed"}}
            return HttpResponse(simplejson.dumps(res), content_type="application/json")

    def new_user(self, request, **kwargs):
        #import pdb;pdb.set_trace()
        try:
            if request.method.lower() == 'post':
                username = request.POST["username"]
                #email = request.POST["email"]
                password = request.POST["password"]
                # firstName = request.POST["firstName"]
                # lastName = request.POST["lastName"]
                # google_id = request.POST["google_id"]
                # facebook_id = request.POST["facebook_id"]
                # google_image = request.POST["google_image"]
                # dob = request.POST["dob"]
                isactive = False
                email = ""

                if '@' in username:
                    email = username
                    user = User.objects.filter(email=email)
                #         raise CustomBadRequest(
                #             code="duplicate_exception",
                #             message="That email is already used.")
                if username:
                    user = User.objects.filter(username=username)
                if user:
                    return HttpResponse("Username/Email already exist Try again")
                else:
                    user_obj, new_user = User.objects.get_or_create(username=username, email=email,is_active=isactive)
                    user_obj.set_password(password)
                    user_obj.save()
                    if user_obj:
                        opt_random = randint(0,999999)
                        otp_create, otp_true = OneTimePassword.objects.get_or_create(user=user_obj, otp=opt_random)
                        #up_create, upp_true = UserProfile.objects.get_or_create(user=user_obj)
                        res = {"result": {"status": "True", "otp_data": otp_create.otp}}
                        return HttpResponse(simplejson.dumps(res), content_type="application/json")
            else:
                res = {"result": {"status": "False", "message": "Method Not allowed"}}
                return HttpResponse(simplejson.dumps(res), content_type="application/json")
        except:
            res = {"result": {"status": "False", "message": "Something went Wrong "}}
            return HttpResponse(simplejson.dumps(res), content_type="application/json")


    def user_login(self, request, **kwargs):
        #import pdb;pdb.set_trace()
        try:
            if request.method.lower() == 'post':
                username = request.POST['username']
                password = request.POST["password"]

                if username and password:
                    user = authenticate(username=username, password=password)

                    #user = User.objects.filter(username=username, password=password)
                    if user.is_active:
                        login(request, user)
                        cards = WalletCard.objects.filter(user=user)
                        user_result = {}
                        user_result['username'] = user.username
                        user_result['first_name'] = user.first_name
                        user_result['last_name'] = user.last_name
                        card_list = []
                        retailers =  Retailer.objects.all()
                        retailers_list = []
                        for retailer in retailers:

                            retailer_values = {}
                            retailer_values['name'] = retailer.name
                            retailer_values['logo'] = retailer.logo
                            #card_values['profile_name'] = wcard.card.card_profile.name
                            #card_values['retailer'] = wcard.card.card_profile.retailer.name
                            #card_values['logo'] = wcard.card.card_profile.retailer.logo
                            #card_values['site_url'] = wcard.card.card_profile.retailer.site_url

                            retailers_list.append(retailer_values)

                        if cards:

                            for wcard in cards:
                                card_values = {}
                                card_values['card_id'] = wcard.card.id
                                card_values['number'] = wcard.card.number
                                card_values['pin'] = wcard.card.pin
                                card_values['profile_name'] = wcard.card.card_profile.name
                                card_values['retailer'] = wcard.card.card_profile.retailer.name
                                card_values['logo'] = wcard.card.card_profile.retailer.logo
                                card_values['site_url'] = wcard.card.card_profile.retailer.site_url
                                retailers = serializers.serialize("json", Retailer.objects.all())
                                card_list.append(card_values)

                        user_result['cards'] = card_list
                        user_result['retailers'] = retailers_list
                        res = {"result": {"status": "True", "user": user_result, "message": "Login success"}}
                        return HttpResponse(simplejson.dumps(res), content_type="application/json")
                    else:
                        res = {"result": {"status": "False", "message": "Login Fail"}}
                        return HttpResponse(simplejson.dumps(res), content_type="application/json")
            else:
                res = {"result": {"status": "False", "message": "Method Not allowed"}}
                return HttpResponse(simplejson.dumps(res), content_type="application/json")
        except:
            res = {"result": {"status": "False", "message": "Something went Wrong "}}
            return HttpResponse(simplejson.dumps(res), content_type="application/json")


    def change_password(self, request, **kwargs):

        try:
            if request.method.lower() == 'post':
                res = {"result": {"status": "True", "message": "Card Added"}}
                return HttpResponse(simplejson.dumps(res), content_type="application/json")

            else:
                res = {"result": {"status": "False", "message": "Method Not allowed"}}
                return HttpResponse(simplejson.dumps(res), content_type="application/json")
        except:
            res = {"result": {"status": "False", "message": "Something went Wrong "}}
            return HttpResponse(simplejson.dumps(res), content_type="application/json")


    def get_cards(self, request, **kwargs):
        try:
            if not request.user:
                res = {"result": {"status": "False", "message": "User Not allowed"}}
                return HttpResponse(simplejson.dumps(res), content_type="application/json")
            else:
                user = User.objects.filter(username=request.POST["username"]).first()

                request.user = user;

                cards = WalletCard.objects.filter(user=request.user)
                user_result = {}
                user_result['username'] = request.user.username
                user_result['first_name'] = request.user.first_name
                user_result['last_name'] = request.user.last_name
                card_list = []
                if cards:

                    for wcard in cards:
                        card_values = {}
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
                    return HttpResponse(simplejson.dumps(res), content_type="application/json")
                else:
                    res = {"result": {"status": "True", "data": user_result, "message": "No Cards available"}}
                    return HttpResponse(simplejson.dumps(res), content_type="application/json")
        except:
            res = {"result": {"status": "False", "message": "Something went Wrong "}}
            return HttpResponse(simplejson.dumps(res), content_type="application/json")

    def new_card(self, request, **kwargs):
        try:
            #if not request.user:
            #res = {"result": {"status": "False", "message": "User Not allowed"}}
            #return HttpResponse(simplejson.dumps(res), content_type="application/json")
            if request.method.lower() == 'post':
                #import pdb;pdb.set_trace()
                # username = request.POST['username']
                # user_obj = User.objects.filter(username=username).first()
                name = request.POST["name"]
                number = request.POST["number"]
                retailer_name = request.POST["retailer"]
                user = User.objects.filter(username=request.POST["user"]).first()
                retailer = Retailer.objects.filter(name=request.POST["retailer"]).first()
                request.user = user;
                pin = request.POST["pin"]
                if request.POST.get("expiration_date"):
                    from time import mktime, strptime
                    exp_date = datetime.strptime(request.POST["expiration_date"], "%Y-%m-%d")
                else:
                    exp_date = ''

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
                            pin=pin,
                            expiration_date=expiration_date)
                    if add_card_obj:
                        card_details = {"number": number, "pin": pin, "type": retailer_name}
                        if request.POST.get("balance"):
                            bal = request.POST["balance"]
                        else:
                            bal_obj = BalanceCheck()
                            bal = bal_obj.card_balance(card_details)
                        card_b = CardBalance()
                        card_b.card = add_card_obj
                        card_b.balance = bal
                        card_b.save()

                    if add_card_obj and request.user:
                        wallet_card = WalletCard.objects.filter(card=add_card_obj, user=request.user)
                        if not wallet_card:
                            wallet_obj, wall = WalletCard.objects.get_or_create(card=add_card_obj, user=request.user)
                            res = {"result": {"status": "True", "message": "Card Entered Success"}}
                            return HttpResponse(simplejson.dumps(res), content_type="application/json")
                        else:
                            res = {"result": {"status": "True", "message": "Card Already mapped"}}
                            return HttpResponse(simplejson.dumps(res), content_type="application/json")
            else:
                res = {"result": {"status": "False", "message": "User Not allowed"}}
                return HttpResponse(simplejson.dumps(res), content_type="application/json")

        except:
            res = {"result": {"status": "False", "message": "User Not allowed"}}
            return HttpResponse(simplejson.dumps(res), content_type="application/json")
