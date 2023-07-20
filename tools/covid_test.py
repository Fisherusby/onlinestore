import datetime

import requests
from bs4 import BeautifulSoup as BS


def get_covid_month(year, month):
    url = f"https://index.minfin.com.ua/reference/coronavirus/geography/belarus/{year}-{month:02}/"
    r = requests.get(url)
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
                "recovered": line_stad_fields[3].getText(),
                "sick": line_stad_fields[4].getText(),
            }
            result.append(stat_by_day)
    return result


def get_covid_all():
    year = 2020
    month = 3
    result = []
    while not ((year == 2022) and (month == 2)):
        result += get_covid_month(year, month)
        print(month, year)
        month += 1
        if month == 13:
            month = 1
            year += 1

    return result
