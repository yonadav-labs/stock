# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from general.models import *
from general.forms import *

def home(request):
    if request.method == 'POST':
        form = OutputForm(request.POST)

        if form.is_valid():
            form.save()
            symbol = form.cleaned_data['symbol']
            inputs = StockInput.objects.filter(symbol=symbol)
    else:
        form = OutputForm()
        inputs = StockInput.objects.all()

    return render(request, 'index.html', {
        'form': form,
        'range_discount': range(1, 26),
        'inputs': inputs,
    })

def get_input_body(request):
    symbol = request.GET.get('symbol')
    if symbol:
        inputs = StockInput.objects.filter(symbol=symbol)
        can_submit = True if inputs else False
    else:
        inputs = StockInput.objects.all()
        can_submit = False

    html = render_to_string('_input.html', { 'inputs': inputs })

    return JsonResponse({'html': html, 'can_submit': can_submit}, safe=False)
