import simplejson

from django.contrib.auth.models import User
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie.authentication import SessionAuthentication
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.http import HttpUnauthorized
from tastypie import fields
from tastypie.resources import ModelResource
from app.utils.balance_check import *

from app.models import *


class WalletCardResource(ModelResource):
    class Meta:
        resource_name = 'wallet'
        queryset = WalletCard.objects.all()
        allowed_methods = ['get','post']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/balance%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('wallet_balance_alert'), name="api_wallet_balance_alert"),
            ]

    def wallet_balance_alert(self, request, **kwargs):

        try:
            #import pdb;pdb.set_trace()
            if not request.user.username:
                res = {"result": {"status": "False", "message": "User Not Login"}}
                return self.create_response(request, res)
            if request.method.lower() in ['get']:
                card_id = request.GET['card_id']
                if card_id:
                    card_obj = Card.objects.filter(id=card_id).first()
                    if card_obj:
                        wallet_card = WalletCard.objects.filter(user=request.user, card=card_obj)
                        if wallet_card:
                            card_details = {"number": card_obj.number, "pin": card_obj.pin,
                            "type": card_obj.card_profile.retailer.name}
                            bal_obj = BalanceCheck()
                            bal = bal_obj.card_balance(card_details)
                            mes = ''
                            if bal:
                                mes = "Your card balance is now" + str(bal)
                                wba= WalletCardBalanceAlert()
                                wba.wallet_card = wallet_card
                                wba.trigger_balance = bal
                                wba.message = mes
                                wba.save()
                            res = {"result": {"status": "True", "message": mes}}
                        else:
                            res = {"result": {"status": "False", "message": "Wallet Card Not match"}}
                    else:
                        res = {"result": {"status": "False", "message": "Card Does not Exist "}}
   
        except:
            res = {"result": {"status": "False", "message": "User Not allowed"}}
        return self.create_response(request, res)

