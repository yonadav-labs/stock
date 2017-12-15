# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from general.models import *
from general.forms import *

def home(request):
    return render(request, 'stock_list.html', {
        'inputs': IssueTable.objects.all()
    })

def issue_offer(request, symbol):
    if request.method == 'POST':
        form = OutputForm(request.POST)
        if form.is_valid():
            form.save()

    form = OutputForm(initial={
        'symbol': symbol,
        'min_price': 0
    })

    offers = []
    for ii in OfferList.objects.filter(symbol=symbol):
        offer = model_to_dict(ii)
        offer['timestamp'] = ii.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        offer['discounted_price'] = discount_price(offer)
        offers.append(offer)

    offers = sorted(offers, key=lambda k: k['discounted_price']) 
    return render(request, 'issue_offer.html', {
        'form': form,
        'range_discount': range(1, 26),
        'range_madays': range(5, 31, 5),
        'ii': IssueTable.objects.get(symbol=symbol),
        'outputs': offers
    })
    
def offer_list(request, symbol):
    offers = []
    for ii in OfferList.objects.filter(symbol=symbol):
        offer = model_to_dict(ii)
        offer['timestamp'] = ii.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        offer['discounted_price'] = discount_price(offer)
        offers.append(offer)

    offers = sorted(offers, key=lambda k: k['discounted_price']) 
    
    return render(request, 'offer_list.html', {
        'outputs': offers
    })

def discount_price(soutput):
    if soutput['ft_type'] == 'FTS':
        sinput = IssueTable.objects.get(symbol=soutput['symbol'])
        discounted_price = sinput.last * (100 - soutput['discount']) / 100
        return discounted_price
    else:
        ph = PriceHistory.objects.filter(symbol=soutput['symbol']).order_by('-date')[:soutput['ma_days']]
        if ph:
            av = 0                
            for ii in ph:
                av += ii.close
            return av/soutput['ma_days']
        return -100000000

@csrf_exempt
def delete_offer(request):
    oid = request.POST.get('id')
    OfferList.objects.filter(id=oid).delete()
    return HttpResponse('')

@csrf_exempt
def delete_history(request):
    symbol = request.POST.get('symbol')
    PriceHistory.objects.filter(symbol=symbol).delete()
    return HttpResponse('')

@csrf_exempt
def update_history(request):
    symbol = request.POST.get('symbol')
    _update_history(symbol)
    return HttpResponse('')

def _update_history(symbol):
    path = '/root/work/stock/data/{}.csv'.format(symbol.upper())
    try:
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    PriceHistory.objects.get_or_create(symbol=symbol,
                                                       open=row['Open'],
                                                       high=row['High'],
                                                       low=row['Low'],
                                                       close=row['Close'],
                                                       date=row['Date'])
                except Exception as e:
                    print e
    except Exception as e:
        print e, '######### no file '

@csrf_exempt
def update_history_all(request):
    for ii in IssueTable.objects.all():
        _update_history(ii.symbol)

    return HttpResponse('')
