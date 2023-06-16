from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.info.models import ExchangeCurrency


class CurrencyAPITestCase(APITestCase):
    def setUp(self):
        self.exchange_1 = ExchangeCurrency.objects.create(
            currency="USD",
            rate=2.54,
            scale=1,
            date="2022-01-07",
        )
        self.exchange_2 = ExchangeCurrency.objects.create(
            currency="EUR",
            rate=3.01,
            scale=1,
            date="2022-01-07",
        )
        self.exchange_3 = ExchangeCurrency.objects.create(
            currency="RUB",
            rate=3.33,
            scale=100,
            date="2022-01-07",
        )

    def test_get_currency_today(self):
        response = self.client.get(reverse("ExchangeCurrencyViewSet-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_exist_currency_detail(self):
        response = self.client.get(
            reverse("ExchangeCurrencyViewSet-detail", args=["EUR"])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_exist_currency_detail(self):
        response = self.client.get(
            reverse("ExchangeCurrencyViewSet-detail", args=["FRT"])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EmptyDBCurrencyAPITestCase(APITestCase):
    def setUp(self):
        pass

    def test_get_currency_today(self):
        response = self.client.get(reverse("ExchangeCurrencyViewSet-list"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_currency_detail(self):
        response = self.client.get(
            reverse("ExchangeCurrencyViewSet-detail", args=["EUR"])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
