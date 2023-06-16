from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from uuslug import uuslug


class Category(MPTTModel):
    name = models.CharField(max_length=128, unique=True, verbose_name="Название")
    description = models.CharField(
        max_length=512, verbose_name="Описание", null=True, blank=True
    )
    slug = models.SlugField(verbose_name="slug", unique=True, max_length=255)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская категория",
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
