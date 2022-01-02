from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from store.models import Product, ReviewProduct, FavoriteProduct
from store.serializers import ProductSerializer, ReviewProductSerializer, ProductReviewsSerializer
from store.serializers.product import ProductToFavoriteSerializer


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'category__slug'

    def get_queryset(self):
        #import pdb
        #pdb.set_trace()
        return self.queryset.filter(category__slug=self.kwargs['cat_slug'])

    def get_object(self):
        # import pdb
        # pdb.set_trace()
        try:
            return self.queryset.get(slug=self.kwargs['slug'])
        except ObjectDoesNotExist:
            raise Http404


class ReviewProductViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductReviewsSerializer
    lookup_field = 'slug'

    def get_object(self):
        # import pdb
        # pdb.set_trace()
        try:
            return self.queryset.get(slug=self.kwargs['slug'])
        except ObjectDoesNotExist:
            raise Http404


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
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        favorite = get_object_or_404(FavoriteProduct, user=request.user, product__slug=self.kwargs['slug'])
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





