import datetime

import requests
from bs4 import BeautifulSoup as BS

from apps.info.models import Covid


def update_covid():
    today = datetime.date.today()
    last_covid = Covid.objects.order_by("date").last()

    if not last_covid:
        from tools.covid19 import covid_add

        covid_add()
        last_covid = Covid.objects.order_by("date").last()
        if not last_covid:
            return False

    if today == last_covid.date:
        return True

    year = int(last_covid.date.strftime("%Y"))
    month = int(last_covid.date.strftime("%m"))

    today_year = int(today.strftime("%Y"))
    today_month = int(today.strftime("%m"))

    tmp_covid = []

    while not ((today_year == year) and (today_month == month)):
        covid_data = get_covid_month(year, month)
        if covid_data is not None:
            tmp_covid += covid_data

        month += 1
        if month == 13:
            month = 1
            year += 1

    covid_data = get_covid_month(today_year, today_month)
    if covid_data is not None:
        tmp_covid += covid_data

    for covid_day in tmp_covid:
        date = f"{covid_day['date'][-4:]}-{covid_day['date'][3:5]}-{covid_day['date'][0:2]}"
        date_time_obj = datetime.datetime.strptime(covid_day["date"], "%d.%m.%Y")
        if date_time_obj.date() > last_covid.date:
            if date_time_obj.date == today:
                return True
            Covid.objects.create(
                date=date,
                infected=int(covid_day["infected"]),
                deaths=int(covid_day["deaths"]),
                recovered=int(covid_day["recovered"]),
                sick=int(covid_day["sick"]),
            )

    return True


def get_try(url, try_count=5):
    while try_count > 0:
        try:
            r = requests.get(url)
            return r
        except Exception as e:
            try_count -= 1
            print(f"Request for {url} error ({e}): next try (less {try_count})")
    return


def get_covid_month(year, month):
    url = f"https://index.minfin.com.ua/reference/coronavirus/geography/belarus/{year}-{month:02}/"

    r = get_try(url)
    if r is None:
        return
    html = BS(r.text, "html.parser")
    body = html

    stat_tbl = body.find("div", {"class": "compact-table"}).find_all("tr")
    result = []
    for line_stat in stat_tbl:
        line_stad_fields = line_stat.find_all("td")

        if len(line_stad_fields) > 1:
            stat_by_day = {
                "date": line_stad_fields[0].getText()[-10:],
                "infected": line_stad_fields[1].getText(),
                "deaths": line_stad_fields[2].getText(),
                "recovered": 0,
                "sick": 0,
            }

            if len(line_stad_fields) > 4:
                stat_by_day["recovered"] = line_stad_fields[3].getText()
                stat_by_day["sick"] = line_stad_fields[4].getText()

            result.append(stat_by_day)
    return result
