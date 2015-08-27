from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api
from app.resources import *
from app.views import *
from app.api import *
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(RetailerResource())
v1_api.register(RetailerCardResource())
v1_api.register(OneTimePasswordResource())
v1_api.register(WalletCardResource())


# Standard bits...
urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
    (r'^api/v1/login', validate_user),
    url(r'^admin/', include(admin.site.urls)),
)
