def update_currncy():
    import json

    import requests

    url = 'https://www.nbrb.by/api/exrates/rates?periodicity=0'

    # CURRENCY = ['USD', 'EUR', 'RUB']

    payload = {}
    headers = {}
    try:
        response = requests.request('GET', url, headers=headers, data=payload)
        json_loads = json.loads(response.text)
        print(type(json_loads))
        if len(json_loads) < 2:
            return False
        for currency in json_loads:
            print(currency)
            date = currency.get('Date', False)
            print(date[:10])

    except requests.ConnectionError:
        return False

    # print(response.text)


update_currncy()
