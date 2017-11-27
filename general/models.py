# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class StockInput(models.Model):
    symbol = models.CharField(max_length=100, primary_key=True)
    last = models.FloatField()
    change = models.FloatField()
    bid = models.FloatField()
    ask = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return self.symbol


FT_TYPE = (
    ('FTS', 'FTS'),
    ('MA', 'MA'),
)

MA_TYPE = (
    ('10D', '10D'),
    ('30D', '30D'),
)

MIN_PRICE = (
    ('NO MIN', 'NO MIN'),
)

DURATION = (
    ('DAY', 'DAY'),
    ('GTC', 'GTC'),
)

class StockOutput(models.Model):
    symbol = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    shares_max = models.IntegerField()
    shares_min = models.IntegerField()
    discount = models.IntegerField()
    ft_type = models.CharField(max_length=50, choices=FT_TYPE)
    ma_type = models.CharField(max_length=50, choices=MA_TYPE)
    min_price = models.CharField(max_length=50, choices=MIN_PRICE)
    duration = models.CharField(max_length=50, choices=DURATION)
    accept_counter_bids = models.BooleanField()
    accept_private_counter_offer = models.BooleanField()

    def __str__(self):
        return '{} - {}'.format(self.symbol, self.action) 
