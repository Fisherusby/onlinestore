from rest_framework import serializers
from store.models import Order, GoodsInOrder, Basket, GoodsInBasket
from tools.notify import notify_order


class GoodsInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsInOrder
        fields = (
            'goods',
            'vendor',
            'price',
            'count',
        )


class OrderSerializer(serializers.ModelSerializer):
    goods = GoodsInOrderSerializer(many=True)

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
            'goods',
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
            GoodsInOrder.objects.create(
                order=order,
                goods=gib.goods,
                vendor=gib.offer.vendor,
                price=gib.offer.price,
                count=gib.count,
            )

        # clear basket
        GoodsInBasket.objects.filter(basket=basket).delete()

        # send email to user about order
        notify_order(order)

        return order

