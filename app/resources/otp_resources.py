from decimal import Decimal
import simplejson
import json
from random import randint
import dateutil.parser

from django.conf.urls import url
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from tastypie.utils import trailing_slash
from tastypie import fields
from tastypie.resources import ModelResource, ALL
from tastypie.serializers import Serializer
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization

from app.models import *
from app.utils.send_mail import *


class OneTimePasswordResource(ModelResource):
    class Meta:
        queryset = OneTimePassword.objects.all()
        resource_name = 'otp'
        allowed_methods = ['get','post']
        filtering = { "id" : ALL }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/otp_request/$" % (self._meta.resource_name), self.wrap_view('otp_request'),\
            	name="api_otp_request"),
            url(r"^(?P<resource_name>%s)/verify_otp/$" % (self._meta.resource_name), self.wrap_view('verify_otp'),
            	name="api_verify_otp"),
        ]

    def otp_request(self, request, **kwargs):
        try:
            if request.method.lower() in ['get']:
                username = request.GET['username']
                if username:
                    user = User.objects.filter(username=username).first()
                    if user:
                        otp_type = request.GET.get('otp_type', 'NEW')
                        otp_verify = OneTimePassword.objects.filter(user=user, is_active=True, otp_types = otp_type).first()
                        if not otp_verify:
                            otp_random = randint(1, 999999)
                            otp_verify, otp_true = OneTimePassword.objects.get_or_create(user=user, otp=otp_random, otp_types = otp_type)
                        if otp_verify:
                            user_p = UserProfile.objects.filter(user=user)
                            if user.email:
                                send_mail2(user.email, "OTP", "your OTP is : "+str(otp_verify.otp))
                            if user_p:
                                if user_p[0].mobile:
                                    mobile = user_p[0].mobile
                                    if mobile[0]=='1' and len(mobile)==11:
                                        country=1
                                    else:
                                        country=0
                                    send_sms=send_sms_msg91(mobile, "your OTP is : "+str(otp_random), country)
                            res = {"result": {"status": "True", "otp_data": otp_verify.otp}}
                    else:
                        res = {"result": {"status": "False", "message": "User Does not exist "}}
                else:
                    res = {"result": {"status": "False", "message": "Username Not entered"}}
            else:
                res = {"result": {"status": "False", "message": "Method Not allowed"}}
        except:
            res = {"result": {"status": "False", "message": "Finally Went wrong"}}
        return self.create_response(request, res)

    def verify_otp(self, request, **kwargs):
        res = {}
        try:
            if request.method.lower() in ['post']:
                input_data = json.loads(request.body)
                otp = input_data.get("otp", "")
                username = input_data.get("username", "")
                otp_type = input_data.get('otp_type', 'NEW')
                if username:

                    user = User.objects.filter(username=username).first()
                    if user:
                        otp_verify = OneTimePassword.objects.filter(user=user, otp=otp,
                            is_active=True, otp_types = otp_type).first()
                        if otp_verify:
                            if otp_verify.otp_types == "NEW":
                                user.is_active = True
                                user.save()
                            otp_verify.is_active=False
                            otp_verify.save()
                            res = {"result": {"status": "True", "message": "Verify otp success"}}
                        else:
                            res = {"result": {"status": "False", "message": "Otp verification Failed"}}
                    else:
                        res = {"result": {"status": "False", "message": "user does not exist"}}
            else:
                res = {"result": {"status": "False", "message": "Method Not allowed"}}

        except:
            res = {"result": {"status": "False", "message": "Something Went wrong"}}
        return self.create_response(request, res)
