import datetime

from django import template

from general.models import *

register = template.Library()

@register.filter
def percent_change(sinput):
    percent = sinput.change * 100 / sinput.last
    return '{0}({1:.2f}%)'.format(sinput.change, percent)

@register.filter
def discount(soutput):
    if soutput.ft_type == 'FTS':
        sinput = StockInput.objects.get(symbol=soutput.symbol)
        discounted_price = sinput.last * (100 - soutput.discount) / 100
        return '{0:.2f}'.format(discounted_price)
    return '-'

@register.filter
def count_offers(symbol):
	return StockOutput.objects.filter(symbol=symbol).count()
