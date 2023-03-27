from django.db import models


class Covid(models.Model):
    date = models.DateField()
    infected = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    sick = models.IntegerField()

    class Meta:
        ordering = ['-date']


