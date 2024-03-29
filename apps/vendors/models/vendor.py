from django.conf import settings
from django.db import models
from uuslug import uuslug

from core.base.model import BaseModel
from tools.image_store import get_path_image_store


def vendor_store_path(instance, filename):
    get_path_image_store(filename, 'vendor')


class Vendor(BaseModel):
    name = models.CharField(max_length=128, verbose_name='Название')
    logo = models.ImageField(upload_to=vendor_store_path, verbose_name='Логотип', blank=True, null=True)
    email = models.EmailField(verbose_name='email')
    address = models.CharField(max_length=256, verbose_name='Адрес')
    slug = models.SlugField(verbose_name='sug', max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = uuslug(f'{self.name}', instance=self)
        super().save(*args, **kwargs)

    @property
    def rating(self):
        rng = self.reviews.all().filter(moderation=True).aggregate(models.Avg('rating'))
        return rng['rating__avg']


class ReviewVendor(BaseModel):
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        verbose_name='Продавец',
        related_name='reviews',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='reviews_vendor',
    )
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Рейтинг')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Отзыв')
    moderation = models.BooleanField(default=False, verbose_name='Прешел модерацию')
    create_data = models.DateTimeField(auto_now_add=True)
