from django.db import models
from uuslug import uuslug

from tools.image_store import get_path_image_store


def logo_store_path(instance, filename):
    return get_path_image_store(filename, "brand")


class Brand(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название")
    logo = models.ImageField(upload_to=logo_store_path, verbose_name="Логотип", blank=True, null=True)
    slug = models.SlugField(max_length=255, verbose_name="slug", unique=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = uuslug(f"{self.name}", instance=self)
        super().save(*args, **kwargs)
