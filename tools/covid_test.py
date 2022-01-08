import datetime

import requests
from bs4 import BeautifulSoup as BS

# r = requests.get('https://index.minfin.com.ua/reference/coronavirus/geography/belarus/2022-01/')
# html = BS(r.text, 'html.parser')
# body = html
#
# stat_tbl = body.find('div', {'class': 'compact-table'}).find_all('tr')
#
# for line_stat in stat_tbl:
#
#     line_stad_fields = line_stat.find_all('td')
#     print(line_stad_fields)
#     if len(line_stad_fields) > 1:
#         print(f'{line_stad_fields[0].getText()[-10:]} - {line_stad_fields[1].getText()} - {line_stad_fields[2].getText()} - {line_stad_fields[3].getText()} - {line_stad_fields[4].getText()}')
#
#     # for field in line_stad_fields:
    #     print(field)


def get_covid_month(year, month):
    url = f'https://index.minfin.com.ua/reference/coronavirus/geography/belarus/{year}-{month:02}/'
    r = requests.get(url)
    html = BS(r.text, 'html.parser')
    body = html

    stat_tbl = body.find('div', {'class': 'compact-table'}).find_all('tr')
    result = []
    for line_stat in stat_tbl:

        line_stad_fields = line_stat.find_all('td')

        if len(line_stad_fields) > 1:
            tmp_date = line_stad_fields[0].getText()[-10:]
            date = f'{tmp_date[1:2]}'
            stat_by_day = {
                'date': line_stad_fields[0].getText()[-10:],
                'infected': line_stad_fields[1].getText(),
                'deaths': line_stad_fields[2].getText(),
                'recovered': line_stad_fields[3].getText(),
                'sick': line_stad_fields[4].getText(),

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

# print(get_covid_month(2021,12))

print(get_covid_all())

# class CoronaStat:
#     infected = body.find('strong', {'class': 'gold'})
#     deaths = body.find('strong', {'class': 'red'})
#     recovered = body.find('strong', {'class': 'green'})
#     sick_now = body.find('strong', {'class': 'blue'})
#     tests_done = body.find('strong', {'class': 'teal normal'})
#
#     def get_infected(self):
#         return self.infected.getText()
#
#     def get_deaths(self):
#         return self.deaths.getText()
#
#     def get_recovered(self):
#         return self.recovered.getText()
#
#     def get_sick_now(self):
#         return self.sick_now.getText()
#
#     def get_tests_done(self):
#         return self.tests_done.getText()
#
# c19 = CoronaStat()
#
# c19.get_deaths()