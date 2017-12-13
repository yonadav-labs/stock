# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from general.models import *

class OutPutAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'shares_max', 'shares_min', 'discount', 'ft_type', 'ma_type', 'duration', 'formatted_time']
    search_fields = ['name']

    def formatted_time(self, obj):
    	return obj.timestamp.strftime("%Y-%m-%d %H:%M:%S")

admin.site.register(IssueTable)
admin.site.register(PriceHistory)
admin.site.register(OfferList, OutPutAdmin)
