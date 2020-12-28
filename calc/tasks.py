from __future__ import absolute_import, unicode_literals

from celery import shared_task
from calc.models import Rate
import urllib.request
import json
import ssl


def get_rate(currency):
    """ Updates exchange rates in Rate objects """
    from_usd = f'USD_{currency}'
    to_usd = f'{currency}_USD'

    url = 'https://api.exchangeratesapi.io/latest?base=USD'
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    str_rates = response.read().decode()
    jsrate = json.loads(str_rates)

    from_usd_rate = jsrate['rates'][currency]
    to_usd_rate = 1 / from_usd_rate

    # Update rates in Rate objects
    for exchange in (from_usd, to_usd):
        rate = Rate.objects.get(name=exchange)
        if exchange == from_usd:
            rate.rate = from_usd_rate
        else:   # exchange == to_usd
            rate.rate = to_usd_rate
        rate.save()


@shared_task
def get_rates():

    get_rate('EUR')
    get_rate('RUB')
    get_rate('CNY')
    get_rate('HKD')
    get_rate('SGD')
    get_rate('KRW')
