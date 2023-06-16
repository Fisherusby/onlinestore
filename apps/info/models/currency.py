from django.db import models


class ExchangeCurrency(models.Model):
    currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=7, decimal_places=4)
    scale = models.PositiveIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default="1900-01-01")

    class Meta:
        ordering = ["created_date"]

    def __str__(self):
        return f"{self.currency}: {self.rate} ({self.date})"
