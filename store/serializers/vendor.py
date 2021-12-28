from rest_framework import serializers

from store.models import Vendor

# name = models.CharField(max_length=128, verbose_name='Название')
# logo = models.ImageField(upload_to=vendor_store_path, verbose_name='Логотип', blank=True, null=True)
# site = models.CharField(max_length=128, verbose_name='Сайт')
# email = models.EmailField(verbose_name='email')
# adress = models.CharField(max_length=256, verbose_name='Адрес')
# phone_number = models.CharField(max_length=64, verbose_name='Тел.', blank=True, null=True)
# slug = models.SlugField(verbose_name='sug', max_length=255, unique=True)


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            'id',
            'name',
            'email',
            'adress',
            'slug',
        )