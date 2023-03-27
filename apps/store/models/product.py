from django.db import models
from django.db.models import Avg
from django.conf import settings

from apps.info.tools import convert_price
from tools.image_store import get_path_image_store
from .product_category import Category
from uuslug import uuslug
from .brand import Brand
from .vendor import Vendor


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    model = models.CharField(verbose_name="Модель", max_length=128)
    brand = models.ForeignKey(Brand, verbose_name="Бренд (Производитель)", on_delete=models.CASCADE, related_name='products')
    production = models.IntegerField(default=2020)
    weight = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, default=0)
    height = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, default=0)
    width = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, default=0)
    deep = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, default=0)
    color = models.CharField(max_length=16, default=None, null=True, blank=True)
    color_duble = models.CharField(max_length=16, default=None, null=True, blank=True)
    slug = models.SlugField(verbose_name='slug', max_length=255, unique=True)


    description = models.TextField(blank=True, null=True)

    @property
    def full_name(self):
        return f'{self.category.name} {self.brand.name} {self.model}'

    @property
    def rating(self):
        rng = self.reviews.all().filter(moderation=True).aggregate(Avg('rating'))
        return rng['rating__avg']

    @property
    def max_price(self):
        max_price = {}
        for offer in self.offers.all():
            for cur, val in offer.price_in_currency.items():
                m_pr = max_price.get(cur, val-1)
                if m_pr < val:
                    max_price[cur] = val
        return max_price

    @property
    def min_price(self):
        min_price = {}
        for offer in self.offers.all():
            for cur, val in offer.price_in_currency.items():
                m_pr = min_price.get(cur, val+1)
                if m_pr > val:
                    min_price[cur] = val
        return min_price

    def save(self, *args, **kwargs):
        self.slug = uuslug(f'{self.brand.name} {self.model}', instance=self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.full_name}'


class OfferVendor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='offers')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Продавец', related_name='offers')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")

    @property
    def price_in_currency(self):
        cur_price = convert_price(self.price)
        return cur_price

    def __str__(self):
        return f'{self.vendor.name} - {self.product.full_name}: {self.price}'


def image_store_path(instance, filename):
    return get_path_image_store(filename, 'products')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name="Изображение", upload_to=image_store_path)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.product.full_name} - {self.pk}. {self.image}'


class ReviewProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Рейтинг')
    review_text = models.TextField(verbose_name='Отзыв')
    title = models.CharField(max_length=128, verbose_name='Заголовок отзыва')
    plus = models.TextField(verbose_name='Достоинства')
    minus = models.TextField(verbose_name='Недостатки')
    created_date = models.DateTimeField(auto_now_add=True)
    moderation = models.BooleanField(default=False, verbose_name='Прошел модерацию')


def reviews_image_path(instance, filename):
    return get_path_image_store(filename, 'reviewsproduct')


class PhotoReviewProduct(models.Model):
    review = models.ForeignKey(ReviewProduct, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=reviews_image_path, verbose_name=' Фотограция')


class FavoriteProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_favorites')
    create_date = models.DateTimeField(auto_now_add=True)
