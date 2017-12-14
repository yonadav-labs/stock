# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from general.models import *

class OutPutAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'shares_max', 'shares_min', 'discount', 'ft_type', 'ma_days', 'duration', 'formatted_time']
    search_fields = ['name']

    def formatted_time(self, obj):
        return obj.timestamp.strftime("%Y-%m-%d %H:%M:%S")

class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'close', 'open', 'high', 'low', 'date']
    search_fields = ['symbol']    
    
admin.site.register(IssueTable)
admin.site.register(PriceHistory, PriceHistoryAdmin)
admin.site.register(OfferList, OutPutAdmin)
