from django.db import models

from core.base.model import BaseModel


class ExchangeCurrency(BaseModel):
    currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=7, decimal_places=4)
    scale = models.PositiveIntegerField(default=1)
    date = models.DateField(default="1900-01-01")

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.currency}: {self.rate} ({self.date})"
