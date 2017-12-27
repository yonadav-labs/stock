import datetime

from django import template

from general.models import *

register = template.Library()

@register.filter
def percent_change(sinput):
    ph = PriceHistory.objects.filter(symbol=sinput.symbol).order_by('-date')
    if ph:
        change = sinput.last - ph[0].close
        percent = change * 100 / sinput.last
        return '{0}({1:.2f}%)'.format(change, percent)
    return '-'

@register.filter
def count_offers(symbol):
    return OfferList.objects.filter(symbol=symbol).count()

