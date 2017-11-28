# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from general.models import *
from general.forms import *

def home(request):
    inputs = StockInput.objects.all()

    if request.method == 'POST':
        form = OutputForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = OutputForm()
        
    return render(request, 'index.html', {
        'range_discount': range(1, 26),
        'inputs': inputs
    })
