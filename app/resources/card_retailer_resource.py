
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


from tastypie.serializers import Serializer

from app.models import * 
from app.resources import UserResource


class RetailerCardResource(ModelResource):
    #user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Card.objects.all()
        resource_name = 'card'
        always_return_data = True
        allowed_methods = ['get','post']
        fields = ['number', 'bin', 'expiration_date']

    def prepend_urls(self):
         return [
            url(r"^(?P<resource_name>%s)/add_cards%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('add_cards'), name="add_cards"),
        ]


    def get_card(self, request, **kwargs):
        try:
            if request.method.lower() == 'get':

       
                queryset = Card.objects.all()
        
                objects = []

                for result in queryset:
                    bundle = self.build_bundle(obj=result, request=request)
                    bundle = self.full_dehydrate(bundle)
                    objects.append(bundle)

                object_list = {
                    'result': objects,
                }

                self.log_throttled_access(request)
                return self.create_response(request, object_list)

        except:
            raise Http404("Sorry, no results on that page.")


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
                pin = request.POST["pin"]
                #expiration_date = dateutil.parser.parse(request.POST["expiration_date"])
                expiration_date = '2015-05-08'
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

