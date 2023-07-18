from django.db import models

from core.base.model import BaseModel


class Covid(BaseModel):
    date = models.DateField()
    infected = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    sick = models.IntegerField()

    class Meta:
        ordering = ["-date"]
