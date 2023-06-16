from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet"
    )
    currency = models.CharField(max_length=3, default="BYN", verbose_name="Валюта")
    amount_of_money = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, verbose_name="Количество денег"
    )

    def __str__(self):
        return f"{self.user}: {self.currency} {self.amount_of_money}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_wallet(sender, instance, **kwargs):
    instance.wallet.save()
