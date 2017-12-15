import datetime

from django import template

from general.models import *

register = template.Library()

@register.filter
def percent_change(sinput):
    ph = PriceHistory.objects.filter(symbol=sinput.symbol).order_by('-date')
    if ph:
        lclose = ph[0].close
        change = lclose - ph[1].close
        percent = change * 100 / lclose
        return '{0}({1:.2f}%)'.format(change, percent)
    return '-'

@register.filter
def count_offers(symbol):
    return OfferList.objects.filter(symbol=symbol).count()

@register.filter
def last_close(symbol):
    ph = PriceHistory.objects.filter(symbol=symbol).order_by('-date')
    if ph:
        return ph[0].close
    return '-'
