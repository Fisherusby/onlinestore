from django.db import models
from django.contrib.auth.models import User

from store.models import Product, Vendor


class Order(models.Model):
    STATUS_CHOICES = (
        ('verify', 'Подтверждение'),
        ('payment', 'Оплата'),
        ('delivery', 'Доставка'),
        # ('ready', 'Готов к выдаче'),
        ('completed', 'Выполнен'),
        ('cancel', 'Отменен'),
    )

    PAYMENT_METHOD = (
        ('cash', 'Наличными'),
        ('wallet', 'Кошелек'),
        ('online', 'online'),
    )

    DELIVERY_METHOD = (
        ('pickup', 'Самовывоз'),
        ('courier', 'Курьером'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='verify')
    payment = models.CharField(max_length=16, choices=PAYMENT_METHOD)
    delivery = models.CharField(max_length=16, choices=DELIVERY_METHOD)
    is_confirmed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_deliver = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #      if not self.pk:
    #          self.number = f'#{}'
    #      super().save(*args, **kwargs)

    @property
    def total_price(self):
        result = 0
        for product in self.products.all():
            result += product.price * product.count
        return result

    def __str__(self):
        return f'№{str(self.id).rjust(10, "0")} - {self.user.username} : {self.total_price}'


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='orders')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Продавец', related_name='orders')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    count = models.PositiveIntegerField(default=0, verbose_name='Количество')