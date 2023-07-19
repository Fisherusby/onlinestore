import datetime

from django.core.exceptions import ObjectDoesNotExist

from apps.info.models import ExchangeCurrency

DEFAULT_CURRENCY = (
    "USD",
    "EUR",
    "RUB",
)


def convert_price(price):
    today = datetime.date.today()
    tmp = {}
    try:
        for currency in DEFAULT_CURRENCY:
            tmp[currency] = ExchangeCurrency.objects.filter(currency=currency).latest("created_at")
    except ObjectDoesNotExist:
        return None

    result = {"BYN": price}
    for currency, data in tmp.items():
        result[currency] = round(price * data.scale / data.rate, 2)

    return result


def update_currency():
    import json

    import requests

    today = datetime.date.today()

    lasts = ExchangeCurrency.objects.filter(date=today)

    if lasts:
        return True

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

        for currency in json_loads:
            cur_name = currency.get("Cur_Abbreviation", False)
            cur_scale = currency.get("Cur_Scale", False)
            cur_official_rate = currency.get("Cur_OfficialRate", False)
            date = currency.get("Date", False)

            exchange_currency = ExchangeCurrency.objects.create(
                currency=cur_name,
                rate=cur_official_rate,
                scale=cur_scale,
                date=date[:10],
            )

        return result
    except requests.ConnectionError:
        return False
