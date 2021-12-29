from django.db import models


class ExchangeCurrency(models.Model):
    currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=7, decimal_places=4)
    scale = models.PositiveIntegerField(default=1)
    date_create = models.DateField(auto_created=True)
    date = models.DateField()

    def __str__(self):
        return f'{self.currency}: {self.rate} ({self.date})'


