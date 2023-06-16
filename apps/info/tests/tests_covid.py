import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.info.models import Covid
from apps.info.tools import update_covid


class CovidUpdateAPITestCase(APITestCase):
    def setUp(self):
        pass

    def test_update_covid(self):
        update_covid()

        covid_all = Covid.objects.all()

        covid_first = covid_all.order_by("date").first()
        covid_last = covid_all.order_by("date").last()

        self.assertEqual(datetime.date(2020, 3, 2), covid_first.date)
        self.assertEqual(datetime.date.today(), covid_last.date)

    def test_get_without_data(self):
        response = self.client.get(reverse("CovidViewSet-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CovidAPITestCase(APITestCase):
    def setUp(self):
        update_covid()

    def test_get_covid(self):
        response = self.client.get(reverse("CovidViewSet-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_covid_today(self):
        today = datetime.date.today()
        today_str = today.strftime("%Y-%m-%d")
        response = self.client.get(reverse("CovidViewSet-detail", args=[today_str]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_covid_tomorrow(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")
        response = self.client.get(reverse("CovidViewSet-detail", args=[tomorrow_str]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class CurrencyAPITestCase(APITestCase):
#     def setUp(self):
#         self.exchange_1 = ExchangeCurrency.objects.create(
#             currency='USD',
#             rate=2.54,
#             scale=1,
#             date='2022-01-07',
#         )
#         self.exchange_2 = ExchangeCurrency.objects.create(
#             currency='EUR',
#             rate=3.01,
#             scale=1,
#             date='2022-01-07',
#         )
#         self.exchange_3 = ExchangeCurrency.objects.create(
#             currency='RUB',
#             rate=3.33,
#             scale=100,
#             date='2022-01-07',
#         )
#
#     def test_get_currency_today(self):
#         response = self.client.get(reverse('ExchangeCurrencyViewSet-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get_exist_currency_detail(self):
#         response = self.client.get(reverse('ExchangeCurrencyViewSet-detail', args=['EUR']))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get_not_exist_currency_detail(self):
#         response = self.client.get(reverse('ExchangeCurrencyViewSet-detail', args=['FRT']))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#
# class EmptyDBCurrencyAPITestCase(APITestCase):
#     def setUp(self):
#         pass
#
#     def test_get_currency_today(self):
#         response = self.client.get(reverse('ExchangeCurrencyViewSet-list'))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_get_currency_detail(self):
#         response = self.client.get(reverse('ExchangeCurrencyViewSet-detail', args=['EUR']))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
