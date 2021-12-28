from rest_framework import serializers
from store.models import Category


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        return CategorySerializer(value).data


class CategorySerializer(serializers.ModelSerializer):
    # children = CategorySerializer2(many=True)
    # children = RecursiveField(many=True, required=False)
    children = RecursiveField(many=True, required=False)

    class Meta:
        model = Category
        fields = (
            # 'id',
            'name',
            # 'description',
            'slug',
            'children'
        )


class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


    # def to_representation(self, value):
    #     import pdb
    #     pdb.set_trace()
    #     pass






# class CategorySerializer3(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = (
#             'id',
#             'name',
#             'description',
#             'slug',
#             'children'
#         )
#
#
# class CategorySerializer2(serializers.ModelSerializer):
#     children = CategorySerializer3(many=True)
#
#     class Meta:
#         model = Category
#         fields = (
#             'id',
#             'name',
#             'description',
#             'slug',
#             'children'
#         )




# CategorySerializer.base_fields['subcategories'] = CategorySerializer()

# name = models.CharField(max_length=128, unique=True, verbose_name='Название')
# description = models.CharField(max_length=512, verbose_name="Описание", null=True, blank=True)
# slug = models.SlugField(verbose_name="slug", unique=True, max_length=255)
# parent = TreeForeignKey(


