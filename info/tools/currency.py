from info.models import ExchangeCurrency
from django.core.exceptions import ObjectDoesNotExist

def convert_price(price):
    import datetime
    today = datetime.date.today()

    default_currency = 'USD'
    try:
        curent_currency_rate = ExchangeCurrency.objects.filter(currency=default_currency, date=today).latest('date_create')
    except ObjectDoesNotExist:
        update_currncy()

        return None


    import pdb
    # pdb.set_trace()

    return default_currency, price*curent_currency_rate.rate


def update_currncy():
    import requests
    import json

    url = "https://www.nbrb.by/api/exrates/rates?periodicity=0"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    json.dumps(response.text)

    print(json)



