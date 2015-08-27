#!/usr/bin/python
from random import randint
import simplejson
import feedparser, re
import json
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
from app.models import *


def get_amount(title, regexes):
        for regex in regexes:
            ret = re.findall(regex, title)
            if len(ret) > 0:
                return ret[0]
        return None


class RetailerResource(ModelResource):
    class Meta:
        queryset = Retailer.objects.all()
        resource_name = 'retailer'
        fields = ['name', 'description', 'site_url']
        allowed_methods = ['get', 'post']
        filtering = { "id" : ALL }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/offer%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('retailer_offers'), name="api_retailer_offers"),
            url(r"^(?P<resource_name>%s)/list%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('retailer_list'), name="api_retailer_list"),
            ]

    def retailer_offers(self, request, **kwargs):
        try:
            if request.method.lower() == 'post':
            	retailer = Retailer.objects.filter(name=request.POST["retailer"]).first()
                retailer_list = []
                if retailer:
                    retail_offer_obj = RetailerOffer.objects.filter(retailer=retailer)
                    for retail in retail_offer_obj:
                        re_data = {}
                        
                        re_data['url'] = retail.url
                        re_data['retailer'] = retailer.name
                        re_data['name'] = retail.name
                        re_data['description'] = retail.description
                        re_data['price'] = retail.price
                        retailer_list.append(re_data)
                       
                if retailer_list:
                    print retailer_list
                    return HttpResponse(simplejson.dumps(retailer_list), content_type="application/json")
                else:
                    res = {"result": {"status": "False", "message": "No Data Available"}}
                    return HttpResponse(simplejson.dumps(res), content_type="application/json")
            else:
                res = {"result": {"status": "False", "message": "Choose Retailer "}}
                return HttpResponse(simplejson.dumps(res), content_type="application/json")
        except:
            res = {"result": {"status": "False", "message": "Something Went  Wrong"}}
            return HttpResponse(simplejson.dumps(res), content_type="application/json")

    def retailer_list(self, request, **kwargs):
        try:
            if request.method.lower() == 'get':
                retailers =  Retailer.objects.all()
                retailers_list = []
                for retailer in retailers:

                    retailer_values = {}
                    retailer_values['name'] = retailer.name
                    retailer_values['logo'] = retailer.logo
                    retailers_list.append(retailer_values)

                res = {"result": {"status": "True", "retailers": retailers_list, "message": "success"}}
                return HttpResponse(simplejson.dumps(res), content_type="application/json")
            else:
                res = {"result": {"status": "False", "message": "Choose Retailer "}}
                return HttpResponse(simplejson.dumps(res), content_type="application/json")
        except:
            res = {"result": {"status": "False", "message": "Something Went  Wrong"}}
            return HttpResponse(simplejson.dumps(res), content_type="application/json")