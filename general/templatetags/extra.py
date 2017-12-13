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
def discount(soutput):
    if soutput.ft_type == 'FTS':
        sinput = IssueTable.objects.get(symbol=soutput.symbol)
        discounted_price = sinput.last * (100 - soutput.discount) / 100
        return '{0:.2f}'.format(discounted_price)
    else:
        ph = PriceHistory.objects.filter(symbol=soutput.symbol).order_by('-date')[:soutput.ma_days]
        if ph:
            av = 0                
            for ii in ph:
                av += ii.close
            return '{0:.2f}'.format(av/soutput.ma_days)
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
