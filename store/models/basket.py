from django.db import models
from django.contrib.auth.models import User

from . import OfferVendor


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        result = {}
        products = self.products_in_basket.all()
        for pr in products:
            for cur, price in pr.price_in_currency.items():
                result.setdefault(cur, 0)
                result[cur] += price
        return result

    def __str__(self):
        return f'{self.user.username}'


class ProductInBasket(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='products_in_basket')
    offer = models.ForeignKey(OfferVendor, on_delete=models.CASCADE, related_name='in_baskets')
    count = models.PositiveIntegerField(default=1)

    @property
    def price_in_currency(self):
        result = {}
        for cur, price in self.offer.price_in_currency.items():
            result[cur] = price * self.count
        return result

    @property
    def product(self):
        return self.offer.product

    @property
    def vendor(self):
        return self.offer.vendor




