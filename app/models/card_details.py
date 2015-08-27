from django.db import models
from django.contrib.auth.models import User
from app.models.retailer import Retailer


class CardProfile(models.Model):
    retailer = models.ForeignKey(Retailer)
    name = models.CharField(max_length=250)
    image_url = models.CharField(max_length=500, null=True, blank=True)
    details = models.CharField(max_length=500, null=True, blank=True)
    terms_and_conditions = models.CharField(max_length=500, null=True, blank=True)
    redemption_information = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=500, null=True, blank=True)
    min_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0.0)
    max_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0.0)
    has_expiration_date = models.BooleanField(default=True)
    has_realtime_balance = models.BooleanField(default=True)
    is_usable_online = models.BooleanField(default=True)
    is_usable_in_store = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    has_pin = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)


    def __unicode__(self):
        return str(self.name)

    class Meta:
        db_table = 'card_profile'


class Card(models.Model):
    card_profile = models.ForeignKey(CardProfile)
    number = models.CharField(max_length=50)
    pin = models.CharField(max_length=50, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    barcode = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return str(self.number) + u"/" + str(self.pin)

    class Meta:
        db_table = 'card'


class CardBalance(models.Model):
    is_active = models.BooleanField(default=True)
    card = models.ForeignKey(Card)
    balance = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return str(self.card.number)

    class Meta:
        db_table = 'card_balance'


class WalletCard(models.Model):
    is_active = models.BooleanField(default=True)
    card = models.ForeignKey(Card)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return str(self.user.first_name)

    class Meta:
        db_table = 'wallet_card'


class WalletCardBalanceAlert(models.Model):
    is_active = models.BooleanField(default=True)
    wallet_card = models.ForeignKey(WalletCard)
    message = models.CharField(max_length=250, blank=True, null=True)
    trigger_balance = models.DecimalField(max_digits=8, decimal_places=2,
        null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)


    class Meta:
        db_table = 'wallet_card_balance_alert'




