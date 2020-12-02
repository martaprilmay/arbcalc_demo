from __future__ import absolute_import, unicode_literals

from celery import shared_task
from calc.models import Rate
# import datetime
import urllib.request
import json
import ssl


def get_rate(currency1, currency2):

    key = f'{currency1}_{currency2}'
    url = (
        f'https://free.currconv.com/api/v7/convert?q={key}'
        f'&compact=ultra&apiKey=6cf91d64550051a2b8e1'
    )
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    str_rate = response.read().decode()
    jsrate = json.loads(str_rate)

    rate = jsrate[key]

    rt = Rate.objects.get(name=key)

    rt.rate = rate


def get_rate2(currency):

    exch1 = f'USD_{currency}'
    exch2 = f'{currency}_USD'

    url1 = 'https://api.exchangeratesapi.io/latest?base=USD'
    context = ssl._create_unverified_context()
    response1 = urllib.request.urlopen(url1, context=context)
    str_rate1 = response1.read().decode()
    jsrate1 = json.loads(str_rate1)

    rate1 = jsrate1['rates'][currency]

    rt1 = Rate.objects.get(name=exch1)
    rt1.rate = rate1
    rt1.save()

    url2 = f'https://api.exchangeratesapi.io/latest?base={currency}'
    response2 = urllib.request.urlopen(url2, context=context)
    str_rate2 = response2.read().decode()
    jsrate2 = json.loads(str_rate2)

    rate2 = jsrate2['rates']['USD']

    rt2 = Rate.objects.get(name=exch2)
    rt2.rate = rate2
    rt2.save()


@shared_task
def get_rates():

    get_rate2('EUR')
    get_rate2('RUB')
    get_rate2('CNY')
    get_rate2('HKD')
    get_rate2('SGD')
    get_rate2('KRW')

    # get_rate('USD', 'EUR')
    # get_rate('EUR', 'USD')
    # get_rate('RUB', 'USD')
    # get_rate('USD', 'RUB')
    # get_rate('USD', 'CNY')
    # get_rate('CNY', 'USD')
    # get_rate('USD', 'HKD')
    # get_rate('HKD', 'USD')
    # get_rate('SGD', 'USD')
    # get_rate('USD', 'SGD')
