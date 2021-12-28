from django.db import models
from uuslug import uuslug

from tools.image_store import get_path_image_store


def vendor_store_path(instance, filename):
    get_path_image_store(filename, 'vendor')


class Vendor(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    logo = models.ImageField(upload_to=vendor_store_path, verbose_name='Логотип', blank=True, null=True)
   # site = models.CharField(max_length=128, verbose_name='Сайт')
    email = models.EmailField(verbose_name='email')
    adress = models.CharField(max_length=256, verbose_name='Адрес')
   # phone_number = models.CharField(max_length=64, verbose_name='Тел.', blank=True, null=True)
    slug = models.SlugField(verbose_name='sug', max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = uuslug(f'{self.name}', instance=self)
        super().save(*args, **kwargs)

