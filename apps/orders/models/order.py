from django.conf import settings
from django.db import models

from apps.info.services import convert_price
from apps.store.models.product import Product, Vendor
from core.base.model import BaseModel

PAYMENT_METHOD = (
    ("cash", "Наличными"),
    ("wallet", "Кошелек"),
    ("online", "online"),
)


class Order(BaseModel):
    VERIFY = "verify"
    PAYMENT = "payment"
    DELIVERY = "delivery"
    COMPLETED = "completed"
    CENCEL = "cancel"

    STATUS_CHOICES = (
        (VERIFY, "Подтверждение"),
        (PAYMENT, "Оплата"),
        (DELIVERY, "Доставка"),
        # ('ready', 'Готов к выдаче'),
        (COMPLETED, "Выполнен"),
        (CENCEL, "Отменен"),
    )

    DELIVERY_METHOD = (
        ("pickup", "Самовывоз"),
        ("courier", "Курьером"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="verify")
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
        result = {}
        products = self.products.all()
        for pr in products:
            for cur, price in pr.price_count.items():
                result.setdefault(cur, 0)
                result[cur] += price
        return result

    def __str__(self):
        return f'№{str(self.id).rjust(10, "0")} - {self.user.username} : {self.total_price}'


class ProductInOrder(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ", related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар", related_name="orders")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name="Продавец", related_name="orders")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    count = models.PositiveIntegerField(default=0, verbose_name="Количество")

    @property
    def price_in_currency(self):
        cur_price = convert_price(self.price)
        return cur_price

    @property
    def price_count(self):
        result = {}
        for cur, val in self.price_in_currency.items():
            result[cur] = val * self.count
        return result


class ReceiptOfPayment(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="receipts")
    method = models.CharField(max_length=16, choices=PAYMENT_METHOD)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    detail = models.CharField(max_length=256, default="")
    is_canceled = models.BooleanField(default=False)
    create_data = models.DateTimeField(auto_now=True)
