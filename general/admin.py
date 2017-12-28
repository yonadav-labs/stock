# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import csv
import datetime
import mimetypes

from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.contrib import admin
from django.forms.models import model_to_dict

from general.models import *

class OutPutAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'shares_max', 'shares_min', 'discount', 'ft_type', 'ma_days', 'duration', 'formatted_time']
    search_fields = ['name']

    def formatted_time(self, obj):
        return obj.timestamp.strftime("%Y-%m-%d %H:%M:%S")

class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'open', 'high', 'low', 'close', 'date']
    search_fields = ['symbol']    
    list_filter = ['symbol']    
    actions = ['download_history']

    def download_history(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ids = ','.join([str(item.id) for item in queryset])
        fields = [f.name for f in PriceHistory._meta.get_fields() 
                  if f.name not in ['id', 'is_new']]

        path = datetime.datetime.now().strftime("/tmp/.{}_price_history_%Y_%m_%d_%H_%M_%S.csv".format(queryset[0].symbol))
        self.write_report(queryset, path, fields)
        wrapper = FileWrapper( open( path, "r" ) )
        content_type = mimetypes.guess_type( path )[0]

        response = HttpResponse(wrapper, content_type = content_type)
        response['Content-Length'] = os.path.getsize( path ) 
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str( os.path.basename( path ) ) 
        return response

    download_history.short_description = "Download history as CSV file" 

    def write_report(self, queryset, path, result_csv_fields):
        result = open(path, 'w')
        result_csv = csv.DictWriter(result, fieldnames=result_csv_fields)
        result_csv.writeheader()

        for product in queryset:
            product_ = model_to_dict(product, fields=result_csv_fields)
            for key, val in product_.items():
                if type(val) not in (float, int, long, bool, datetime.date) and val:
                    product_[key] = val.encode('utf-8')
                elif type(val) == datetime.date:
                  product_[key] = str(val)

            # break
            try:
                result_csv.writerow(product_)
            except Exception, e:
                print product_
        result.close()


admin.site.register(IssueTable)
admin.site.register(PriceHistory, PriceHistoryAdmin)
admin.site.register(OfferList, OutPutAdmin)
