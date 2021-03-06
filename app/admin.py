from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import *


class WalletCardInline(admin.TabularInline):
    model = WalletCard
    extra = 1

class RetailerAdmin(admin.ModelAdmin):
	list_display  = ('name', 'is_active',)
	list_filter   = ['is_active',]	
	search_fields = ['name', 'description',]


class RetailerOfferAdmin(admin.ModelAdmin):
	list_display  = ('name', 'is_active',)
	list_filter   = ['is_active',]	
	search_fields = ['name', 'description',]


class CardProfileAdmin(admin.ModelAdmin):
    list_display  = ('name', 'retailer', 'is_active',)
    list_filter   = ['is_active',]
    search_fields = ['name', ]

class RetailerLocationAdmin(admin.ModelAdmin):
    list_display  = ('address', 'address2', 'city', 'state', 'postal_code', 'lat', 'lng', 'retailer', 'is_active',)
    list_filter   = ['is_active', 'retailer', 'state',]
    search_fields = ['address', 'address2', 'city', 'state', 'postal_code', ]

class CardAdmin(admin.ModelAdmin):
	inlines = (WalletCardInline,)
	list_display  = ('number', 'pin', 'expiration_date', 'card_profile',)
	list_filter   = ['card_profile',]
	search_fields = ['number', 'pin']

class CardBalanceAdmin(admin.ModelAdmin):
	list_display  = ('card', 'balance', 'is_active',)
	list_filter   = ['is_active',]
	search_fields = ['card',]

class OtpAdmin(admin.ModelAdmin):
	list_display  = ('otp', 'is_active',)
	list_filter   = ['is_active',]	
	search_fields = ['user', 'otp',]

class WalletCardAdmin(admin.ModelAdmin):
	list_display  = ('user', 'card',)
	list_filter   = ['is_active',]	
	search_fields = ['user', 'card',]


class UserProfileAdmin(admin.ModelAdmin):
 list_display  = ('user',)
 list_filter   = ['user',] 
 search_fields = ['user',]



admin.site.register(WalletCard,  WalletCardAdmin)
admin.site.register(Card,  CardAdmin)
admin.site.register(CardBalance,  CardBalanceAdmin)
admin.site.register(RetailerOffer,  RetailerOfferAdmin)
admin.site.register(Retailer,  RetailerAdmin)
admin.site.register(CardProfile, CardProfileAdmin)
admin.site.register(RetailerLocation, RetailerLocationAdmin)
admin.site.register(OneTimePassword,  OtpAdmin)
admin.site.register(UserProfile,  UserProfileAdmin)
