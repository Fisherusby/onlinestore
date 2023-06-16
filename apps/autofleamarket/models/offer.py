from django.conf import settings
from django.db import models

from apps.autofleamarket import Auto


class OfferAuto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    model = models.ForeignKey(Auto, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()
    body = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    engine = models.CharField(max_length=16)
    transmission = models.CharField(max_length=16)
    drive_unit = models.CharField(max_length=16)
    state = models.CharField(max_length=16)
    is_cleared = models.BooleanField(max_length=16)
    create_date = models.DateTimeField(auto_now=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
