from rest_framework import serializers
from store.models import Order, ProductInOrder, Basket, ProductInBasket
from tools.notify import notify_order


class ProductInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInOrder
        fields = (
            'product',
            'vendor',
            'price',
            'count',
        )


class OrderSerializer(serializers.ModelSerializer):
    products = ProductInOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'create_date',
            'status',
            'is_completed',
            'is_pay',
            'is_cancel',
            'products',
            'total_price',
        )

    def create(self, validated_data):

        # get user basket
        basket = Basket.objects.get(user=self.context['request'].user)

        # if basket empty generate raise
        if not basket.total_price > 0:
            raise serializers.ValidationError("Basket empty")

        # Create new order
        order = Order.objects.create(user=self.context['request'].user)

        # Add goods in order from basket
        for gib in basket.goods_in_basket.all():
            ProductInOrder.objects.create(
                order=order,
                product=gib.product,
                vendor=gib.offer.vendor,
                price=gib.offer.price,
                count=gib.count,
            )

        # clear basket
        ProductInBasket.objects.filter(basket=basket).delete()

        # send email to user about order
        notify_order(order)

        return order

