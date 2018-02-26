# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import subprocess

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from general.models import *
from general.forms import *

def login(request):
    return render(request, 'login.html')
    
def home(request):
    template = '_stock_list.html' if request.is_ajax() else 'stock_list.html'
    return render(request, template, {
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
    
    template = '_offer.html' if request.is_ajax() else 'offer_list.html'
    return render(request, template, {
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
            return av / ph.count() * (100 - soutput['discount']) / 100
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
def run_scraper_value(request):
    path = settings.BASE_DIR + '/general/get_data.py'
    subprocess.Popen(["python", path, "value"])
    return HttpResponse('')

@csrf_exempt
def run_scraper_history(request):
    path = settings.BASE_DIR + '/general/get_data.py'
    subprocess.Popen(["python", path, "history"])
    return HttpResponse('')
