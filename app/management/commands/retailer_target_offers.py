from django.core.management.base import BaseCommand, CommandError
from app.models import *

import feedparser, re

def get_amount(title, regexes):
    for regex in regexes:
        ret = re.findall(regex, title)
        if len(ret) > 0:
            return ret[0]
    return None


class Command(BaseCommand):
    help = 'Loads locations for Target'

    def handle(self, *args, **options):
    	retailer = Retailer.objects.filter(name='Target').first()
    	etailer_list = []
        if retailer.slick_deals_url:
            feed = feedparser.parse(str(retailer.slick_deals_url))
            for entry in feed.entries:
            	try:
                    title = entry.title
                    link = entry.link
                    amount = get_amount(title, [r'\$[\d.]+', r'\$[\d.]+', r'\d\d.\d\d', r'[\d]+.[\d]+'])
                    if amount:
                        re_data = {}
                        try:
                            clean_balance = float(str(amount).replace("$", ""))
                        except:
                            clean_balance = "9.99"
                        retailerOffer = RetailerOffer()
                        retailerOffer.url = link
                        retailerOffer.is_active = True
                        retailerOffer.retailer = retailer
                        retailerOffer.name = title.encode('ascii', 'ignore')[:200]
                        retailerOffer.description = title.encode('ascii', 'ignore')[:200]
                        retailerOffer.price = clean_balance
                        retailerOffer.save()
                except:
                	None

        print "test"