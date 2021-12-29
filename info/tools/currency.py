from info.models import ExchangeCurrency
from django.core.exceptions import ObjectDoesNotExist


def convert_price(price):
    import datetime
    today = datetime.date.today()

    default_currency = 'USD'
    try:
        current_currency_rate = ExchangeCurrency.objects.filter(currency=default_currency, date=today).latest('created_date')
        # import pdb
        # pdb.set_trace()
        return default_currency, price * current_currency_rate.scale / current_currency_rate.rate
    except ObjectDoesNotExist:
        current_currency_rate = update_currecy(default_currency)
        if not current_currency_rate:
            try:
                current_currency_rate = ExchangeCurrency.objects.filter(currency=default_currency).latest('created_date')
                return default_currency, price * current_currency_rate.scale / current_currency_rate.rate
            except ObjectDoesNotExist:
                return None

        return default_currency, price * current_currency_rate


def update_currecy(default_currency):
    import requests
    import json

    result = 0

    url = "https://www.nbrbsdsds.by/api/exrates/rates?periodicity=0"

    # CURRENCY = ['USD', 'EUR', 'RUB']

    payload = {}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        json_loads = json.loads(response.text)
        # print(type(json_loads))
        if len(json_loads) < 2:
            return False
        for currency in json_loads:
            cur_name = currency.get('Cur_Abbreviation', False)
            cur_scale = currency.get('Cur_Scale', False)
            cur_official_rate = currency.get('Cur_OfficialRate', False)
            date = currency.get('Date', False)

            if cur_name == default_currency:
                result = cur_scale/cur_official_rate

            ExchangeCurrency.objects.create(
                currency=cur_name,
                rate=cur_official_rate,
                scale=cur_scale,
                date=date[:10],
            )
        return result
    except requests.ConnectionError:
        return False


