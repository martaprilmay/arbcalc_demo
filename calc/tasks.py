from __future__ import absolute_import, unicode_literals

from celery import shared_task
from calc.models import Rate
# import datetime
import urllib.request
import json
import ssl


def get_rate(currency):

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

    rate2 = 1 / rate1

    rt2 = Rate.objects.get(name=exch2)
    rt2.rate = rate2
    rt2.save()


@shared_task
def get_rates():

    get_rate('EUR')
    get_rate('RUB')
    get_rate('CNY')
    get_rate('HKD')
    get_rate('SGD')
    get_rate('KRW')
