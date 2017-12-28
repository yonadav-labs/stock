# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class IssueTable(models.Model):
    symbol = models.CharField(max_length=100, primary_key=True)
    num_shares_available = models.IntegerField(default=0)
    last = models.FloatField(default=0)
    change = models.FloatField(default=0)
    bid = models.FloatField(default=0)
    ask = models.FloatField(default=0)
    high = models.FloatField(default=0)
    low = models.FloatField(default=0)
    volume = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol


FT_TYPE = (
    ('FTS', 'FTS'),
    ('MA', 'MA'),
)

DURATION = (
    ('DAY', 'DAY'),
    ('GTC', 'GTC'),
)

class OfferList(models.Model):
    symbol = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    shares_max = models.IntegerField()
    shares_min = models.IntegerField()
    discount = models.IntegerField()
    ft_type = models.CharField(max_length=50, choices=FT_TYPE)
    ma_days = models.IntegerField(default=0, null=True, blank=True)
    min_price = models.FloatField()
    duration = models.CharField(max_length=50, choices=DURATION)
    accept_counter_bids = models.BooleanField()
    accept_private_counter_offer = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.symbol, self.action) 


class PriceHistory(models.Model):
    symbol = models.CharField(max_length=100)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return self.symbol
