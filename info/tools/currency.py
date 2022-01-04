from info.models import ExchangeCurrency
from django.core.exceptions import ObjectDoesNotExist


def convert_price(price, currency='USD'):
    import datetime
    today = datetime.date.today()

    # default_currency = 'USD'
    try:
        current_currency_rate = ExchangeCurrency.objects.filter(currency=currency, date=today).latest('created_date')
        # return price * current_currency_rate.scale / current_currency_rate.rate
    except ObjectDoesNotExist:
        current_currency_rate = update_currency(currency)
        if not current_currency_rate:
            try:
                current_currency_rate = ExchangeCurrency.objects.filter(currency=currency).latest('created_date')
                # return price * current_currency_rate.scale / current_currency_rate.rate
            except ObjectDoesNotExist:
                return None

    return price * current_currency_rate.scale / current_currency_rate.rate


def update_currency(default_currency):
    import requests
    import json

    result = True

    url = "https://www.nbrb.by/api/exrates/rates?periodicity=0"

    # CURRENCY = ['USD', 'EUR', 'RUB']

    payload = {}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        json_loads = json.loads(response.text)

        if len(json_loads) < 2:
            return False

        # {"Cur_ID": 440, "Date": "2022-01-03T00:00:00", "Cur_Abbreviation": "AUD", "Cur_Scale": 1,
        #          "Cur_Name": "Австралийский доллар", "Cur_OfficialRate": 1.8492}

        for currency in json_loads:
            cur_name = currency.get('Cur_Abbreviation', False)
            cur_scale = currency.get('Cur_Scale', False)
            cur_official_rate = currency.get('Cur_OfficialRate', False)
            date = currency.get('Date', False)

            exchange_currency = ExchangeCurrency.objects.create(
                currency=cur_name,
                rate=cur_official_rate,
                scale=cur_scale,
                date=date[:10],
            )

            if cur_name == default_currency:
                result = exchange_currency

        return result
    except requests.ConnectionError:
        return False