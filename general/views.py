# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from general.models import *
from general.forms import *

def home(request):
    return render(request, 'i_table.html', {
        'inputs': IssueTable.objects.all()
    })

def i_post(request, symbol):
    if request.method == 'POST':
        form = OutputForm(request.POST)

        if form.is_valid():
            form.save()
            
    form = OutputForm(initial={
        'symbol': symbol,
        'min_price': 0
    })

    return render(request, 'i_post.html', {
        'form': form,
        'range_discount': range(1, 26),
        'range_madays': range(5, 31, 5),
        'ii': IssueTable.objects.get(symbol=symbol),
        'outputs': OfferList.objects.filter(symbol=symbol)
    })
    
def i_posts(request, symbol):
    return render(request, 'i_posts.html', {
        'outputs': OfferList.objects.filter(symbol=symbol)
    })

@csrf_exempt
def delete_offer(request):
    oid = request.POST.get('id')
    OfferList.objects.filter(id=oid).delete()
    return HttpResponse('')

def import_pricehistory(request):
    for ii in IssueTable.objects.all():
        path = '/root/work/stock/data/{}.csv'.format(ii.symbol.upper())
        try:
            with open(path) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        PriceHistory.objects.get_or_create(symbol=ii.symbol,
                                                           open=row['Open'],
                                                           high=row['High'],
                                                           low=row['Low'],
                                                           close=row['Close'],
                                                           date=row['Date'])
                    except Exception as e:
                        print e
        except Exception as e:
            print e, '######### no file '

    return HttpResponse('Successfully Imported')
