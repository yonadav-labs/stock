from django import template
import datetime

register = template.Library()

@register.filter
def percent_change(sinput):
    percent = sinput.change * 100 / sinput.last
    return '{0}({1:.2f}%)'.format(sinput.change, percent)
