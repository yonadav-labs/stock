import os
import django
import urllib2

from lxml import html
from os import sys, path
from datetime import datetime

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock.settings")
django.setup()

from general.models import *

def get_issue(issue):
    url = 'https://finance.yahoo.com/quote/{}/'.format(issue.symbol.upper())
    content = urllib2.urlopen(url).read()
    tree = html.fromstring(content)

    issue.last = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span/text()')[0]
    issue.bid = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]/text()')[0].split(' ')[0]
    issue.ask = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[4]/td[2]/text()')[0].split(' ')[0]
    issue.volume = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span/text()')[0].replace(',', '')
    issue.save()

def get_history(issue):
    url = 'https://finance.yahoo.com/quote/{}/history'.format(issue.symbol.upper())
    content = urllib2.urlopen(url).read()
    tree = html.fromstring(content)
    
    trs = tree.xpath('//*[@data-test="historical-prices"]/tbody/tr')
    for tr in trs:
        _, created = PriceHistory.objects.get_or_create(symbol=issue.symbol,
                                                        open=tr.xpath('./td[2]/span/text()')[0],
                                                        high=tr.xpath('./td[3]/span/text()')[0],
                                                        low=tr.xpath('./td[4]/span/text()')[0],
                                                        close=tr.xpath('./td[5]/span/text()')[0],
                                                        date=datetime.strptime(tr.xpath('./td[1]/span/text()')[0], '%b %d, %Y').strftime('%Y-%m-%d'))

        if not created:
            break

if __name__ == '__main__':
    for ii in IssueTable.objects.all():
        get_issue(ii)
        get_history(ii)
