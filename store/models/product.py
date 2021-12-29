from django.db import models
from django.db.models import Avg, Max, Min

from info.tools import convert_price
from tools.image_store import get_path_image_store
from .product_category import Category
from uuslug import uuslug
from .brand import Brand
from .vendor import Vendor
from django.contrib.auth.models import User


# class Product(models.Model):
#     name = models.CharField(verbose_name="Название", max_length=128, unique=True)
#     description = models.CharField(verbose_name="Описание", max_length=512, null=True, blank=True)
#     category = models.ForeignKey(
#         Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория'
#     )
#     slug = models.SlugField(verbose_name='slug', max_length=255, unique=True)
#
#     def save(self, *args, **kwargs):
#         self.slug = uuslug(self.name, instance=self)
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return f'{self.name}'


class Goods(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='goods', verbose_name="Категория")
    model = models.CharField(verbose_name="Модель", max_length=128, unique=True)
    brand = models.ForeignKey(Brand, verbose_name="Бренд (Производитель)", on_delete=models.CASCADE, related_name='goods')
    slug = models.SlugField(verbose_name='slug', max_length=255, unique=True)

    @property
    def full_name(self):
        return f'{self.category.name} {self.brand.name} {self.model}'

    @property
    def rating(self):
        rng = self.reviews.all().filter(moderation=True).aggregate(Avg('rating'))
        return rng['rating__avg']

    @property
    def max_price(self):
        max_price = self.offers.all().aggregate(Max('price'))
        return max_price['price__max']

    @property
    def min_price(self):
        min_price = self.offers.all().aggregate(Min('price'))
        return min_price['price__min']

    def save(self, *args, **kwargs):
        self.slug = uuslug(f'{self.brand.name} {self.model}', instance=self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.category.name} - {self.brand.name} {self.model}'


class OfferVendor(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='Товар', related_name='offers')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Продавец', related_name='offers')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")

    @property
    def price_currency(self):
        return convert_price(self.price)

    def __str__(self):
        return f'{self.vendor.name} - {self.goods.category.name} {self.goods.brand.name} {self.goods.model}: {self.price}'


def image_store_path(instance, filename, name):
    return get_path_image_store(filename, 'goods')


class GoodsImage(models.Model):
    goods = models.ForeignKey(Goods, verbose_name="Товар", on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name="Изображение", upload_to=image_store_path)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.goods.category.name} {self.goods.model} - {self.pk}. {self.image}'


class ReviewGoods(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Рейтинг')
    review_text = models.TextField(verbose_name='Отзыв')
    title = models.CharField(max_length=128, verbose_name='Заголовок отзыва')
    plus = models.TextField(verbose_name='Достоинства')
    minus = models.TextField(verbose_name='Недостатки')
    created_date = models.DateTimeField(auto_created=True)
    moderation = models.BooleanField(default=False, verbose_name='Прошел модерацию')


def reviews_image_path(instance, filename):
    return get_path_image_store(filename, 'reviewsgoods')


class PhotoReviewGoods(models.Model):
    review = models.ForeignKey(ReviewGoods, on_delete=models.CASCADE, related_name='photos')
    photos = models.ImageField(upload_to=reviews_image_path, verbose_name=' Фотограция')





#
# class PropertyProduct(models.Model):
#     title = models.CharField(max_length=128, verbose_name="Наименование хорактеристики")
#     store = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
#     description = models.CharField(max_length=255, verbose_name="Описание", null=True, blank=True)
#
#     def __str__(self):
#         return f'{self.store.name} - {self.title}'
#
#
# class Goods(models.Model):
#     product_type = models.ForeignKey(Product, verbose_name="Тип продукта", on_delete=models.CASCADE)
#     prise = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена за еденицу")
#     brand = models.CharField(max_length=64, verbose_name="Производитель (бренд)")
#     model = models.CharField(max_length=128, verbose_name="Модель")
#     year = models.PositiveIntegerField(verbose_name="Дата выхода на рынок")
#
#
# class GoodsProperty(models.Model):
#     value = models.CharField(max_length=64, verbose_name="Значение", null=True, blank=True)
#     goodss = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="Товар")
#     Properties = models.ForeignKey(PropertyProduct, on_delete=models.CASCADE, verbose_name="Характеристика")
#
