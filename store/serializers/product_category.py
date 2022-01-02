from rest_framework import serializers
from store.models import Category


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        return CategorySerializer(value).data


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, required=False)

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
            'children'
        )


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )

