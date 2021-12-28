from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from . import Goods, OfferVendor


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        result = 0
        products = self.goods_in_basket.all()
        for pr in products:
            result += pr.price_sum
        return result

    def __str__(self):
        return f'{self.user.username}'


class GoodsInBasket(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='goods_in_basket')
   # goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='in_baskets')
    offer = models.ForeignKey(OfferVendor, on_delete=models.CASCADE, related_name='in_baskets')
    count = models.PositiveIntegerField(default=0)

    @property
    def price_sum(self):
        return self.offer.price * self.count

    @property
    def goods(self):
        return self.offer.goods

    @property
    def vendor(self):
        return self.offer.vendor




