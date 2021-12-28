from rest_framework import serializers
from store.models import Goods, OfferVendor, ReviewGoods, PhotoReviewGoods
from .vendor import VendorSerializer
from .brand import BrandSerializer
from .product_category import GoodsCategorySerializer


class OfferVendorSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()

    class Meta:
        model = OfferVendor
        fields = (
            'vendor',
            'price',
        )


class GoodsSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = GoodsCategorySerializer()
    offers = OfferVendorSerializer(many=True)

    class Meta:
        model = Goods
        fields = (
            'full_name',
            'category',
            'model',
            'brand',
            'slug',
            'images',
            'offers',
            'rating',
            'min_price',
            'max_price',
        )
        lookup_field = 'slug'


class PhotoReviewGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoReviewGoods
        fields = (
            'photos',
        )


class ReviewGoodsSerializer(serializers.ModelSerializer):
    photos = PhotoReviewGoodsSerializer(many=True)

    class Meta:
        model = ReviewGoods
        fields = (
            'user',
            'rating',
            'review_text',
            'title',
            'plus',
            'minus',
            'created_date',
            'photos',
        )


# class ReviewGoods(models.Model):
#     goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
#     rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Рейтинг')
#     review_text = models.TextField(verbose_name='Отзыв')
#     title = models.CharField(max_length=128, verbose_name='Заголовок отзыва')
#     plus = models.TextField(verbose_name='Достоинства')
#     minus = models.TextField(verbose_name='Недостатки')
#     created_date = models.DateTimeField(auto_created=True)
#     moderation = models.BooleanField(default=False, verbose_name='Прошел модерацию')

