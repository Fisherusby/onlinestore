from django.db import models
from django.contrib.auth.models import User

from store.models import Goods, Vendor


class Order(models.Model):
    STATUS_CHOICES = (
        ('check', 'Подтверждение'),
        ('payment', 'Оплата'),
        ('delivery', 'Доставка'),
        ('ready', 'Готов к выдаче'),
        ('finish', 'Выполнен'),
        ('cancel', 'Отменен'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=64, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='check')
    is_completed = models.BooleanField(default=False)
    is_pay = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #      if not self.pk:
    #          self.number = f'#{}'
    #      super().save(*args, **kwargs)

    @property
    def total_price(self):
        result = 0
        for gds in self.goods.all():
            result += gds.price * gds.count
        return result

    def __str__(self):
        return f'№{str(self.id).rjust(10, "0")} - {self.user.username} : {self.total_price}'


class GoodsInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='goods')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='Товар', related_name='orders')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Продавец', related_name='orders')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    count = models.PositiveIntegerField(default=0, verbose_name='Количество')