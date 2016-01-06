from django.db import models
from django.contrib.auth.models import User

class Retailer(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField()
    logo = models.URLField(max_length=500)
    site_url = models.URLField(max_length=500, blank=True)
    slick_deals_url = models.URLField(null=True, blank=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    balance_check_url = models.CharField(max_length=200, blank=True, null=True)
    
    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "retailer"


class RetailerLocation(models.Model):
    is_active = models.BooleanField(default=True)
    retailer = models.ForeignKey(Retailer)
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lng = models.DecimalField(max_digits=10, decimal_places=6)
    address = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=250)
    
    def __unicode__(self):
        return self.address + " " + self.address2 + " " + self.city + " " + self.state + " , " + self.postal_code

    class Meta:
        db_table = "retailer_locations"


class RetailerOffer(models.Model):
    is_active = models.BooleanField(default=True)
    retailer = models.ForeignKey(Retailer)
    name = models.CharField(max_length=250)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    url = models.URLField(null=True, blank=True, max_length=500)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "retailer_offers"