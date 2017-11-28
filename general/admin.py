# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from general.models import *

class OutPutAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'shares_max', 'shares_min', 'discount', 'ft_type', 'ma_type', 'duration', 'timestamp']
    search_fields = ['name']

admin.site.register(StockInput)
admin.site.register(StockOutput, OutPutAdmin)
