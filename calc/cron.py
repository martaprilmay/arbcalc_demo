# Python libraries
import json
import ssl
import urllib.request

# Local imports
from .models import Rate
from .tasks import get_rate2


def my_scheduled_job():

    get_rate2('EUR')
    get_rate2('RUB')
    get_rate2('CNY')
    get_rate2('HKD')
    get_rate2('SGD')
