import datetime

from info.models import Covid


def covid_update():
    today = datetime.date.today()
    last_covid = Covid.objects.last()

    if today == last_covid.date:
        return True

    year = last_covid.date.year()
    month = last_covid.date.month()
    day = last_covid.date.day()





# def covid_get_update():


