from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.response import Response

from apps.store.models import FavoriteProduct, Product, ReviewProduct
from apps.store.serializers import ProductReviewsSerializer, ProductSerializer
from apps.store.serializers.product import (
    CreateReviewProductSerializer,
    ProductToFavoriteSerializer,
    UpdateReviewProductSerializer,
)


class AllProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "category__slug",
        "brand__slug",
        "color",
        "production",
    ]
    search_fields = [
        "brand__name",
        "model",
        "category__name",
    ]

    ordering_fields = [
        "brand__name",
        "category__name",
        "color",
        "production",
    ]
    lookup_field = "slug"

    # def get_queryset(self):
    #     return self.queryset.filter(category__slug=self.kwargs['cat_slug'])
    #
    # def get_object(self):
    #     try:
    #         return self.queryset.get(slug=self.kwargs['slug'])
    #     except ObjectDoesNotExist:
    #         raise Http404


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['category', 'in_stock']
    search_fields = ["full_name"]

    def get_queryset(self):
        return self.queryset.filter(category__slug=self.kwargs["cat_slug"])

    def get_object(self):
        try:
            return self.queryset.get(slug=self.kwargs["slug"])
        except ObjectDoesNotExist:
            raise Http404


class ProductReviewsViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductReviewsSerializer
    lookup_field = "slug"

    def get_object(self):
        try:
            return self.queryset.get(slug=self.kwargs["slug"])
        except ObjectDoesNotExist:
            raise Http404


class ReviewProductViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = ReviewProduct.objects.all()
    serializers = {
        "create": CreateReviewProductSerializer,
        "update": UpdateReviewProductSerializer,
        "partial_update": UpdateReviewProductSerializer,
    }

    def get_serializer_class(self):
        # import pdb
        # pdb.set_trace()
        return self.serializers[self.action]


class FavoriteProductsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(in_favorites__user=self.request.user)


class ProductToFavoriteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductToFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"

    def destroy(self, request, *args, **kwargs):
        favorite = get_object_or_404(FavoriteProduct, user=request.user, product__slug=self.kwargs["slug"])
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
