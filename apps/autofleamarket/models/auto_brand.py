import datetime

from django.conf import settings
from django.db import models
from uuslug import uuslug

from core.base.model import BaseModel
from tools.image_store import get_path_image_store


def auto_brand_store_path(instance, filename):
    get_path_image_store(filename, 'auto_brand')


class AutoBrand(BaseModel):
    name = models.CharField(max_length=64)
    logo = models.ImageField(upload_to=auto_brand_store_path, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = uuslug(f'{self.name}', instance=self)
        super().save(*args, **kwargs)


class AutoLineModel(BaseModel):
    name = models.CharField(max_length=64)
    brand = models.ForeignKey(AutoBrand, on_delete=models.CASCADE, related_name='model_lines')


def year_choices():
    return [(r, r) for r in range(1900, datetime.date.today().year + 1)]


def current_year():
    return datetime.date.today().year


class Auto(BaseModel):
    YEAR_CHOICES = [(r, r) for r in range(1900, datetime.date.today().year + 1)]

    model = models.CharField(max_length=64)
    line_model = models.ForeignKey(AutoLineModel, on_delete=models.CASCADE, related_name='models')
    start_production = models.IntegerField(('year'), choices=year_choices(), default=current_year())
    end_production = models.IntegerField(('year'), choices=year_choices(), default=current_year())

    def __str__(self):
        return f'{self.line_model.brand.name} {self.line_model.name} {self.model}'


class ReviewAuto(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='AutoReviews', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    review = models.TextField()
    plus = models.CharField(max_length=256)
    minus = models.CharField(max_length=256)
    rating_hod = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Рейтинг')
    rating_komf = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Рейтинг')
    rating_nade = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Рейтинг')
    rating_odsl = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Рейтинг')
    rating_cost = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Рейтинг')

    def rating(self):
        return round(
            (self.rating_cost + self.rating_hod + self.rating_odsl + self.rating_nade + self.rating_komf) / 5,
            1,
        )
