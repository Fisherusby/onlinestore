from rest_framework import serializers
from store.models import Order, ProductInOrder, Basket, ProductInBasket
from tools.notify import notify_order
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


class ProductInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInOrder
        fields = (
            'product',
            'vendor',
            'price',
            'count',
        )


    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # create_date = models.DateTimeField(auto_now_add=True)
    # status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='verify')
    # payment = models.CharField(max_length=16, choices=PAYMENT_METHOD)
    # delivery = models.CharField(max_length=16, choices=DELIVERY_METHOD)
    # is_confirmed = models.BooleanField(default=False)
    # is_paid = models.BooleanField(default=False)
    # is_deliver = models.BooleanField(default=False)
    # is_completed = models.BooleanField(default=False)
    # is_cancel = models.BooleanField(default=False)

class OrderSerializer(serializers.ModelSerializer):
    products = ProductInOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'create_date',
            'status',
            'payment',
            'delivery',
            'is_confirmed',
            'is_paid',
            'is_deliver',
            'is_completed',
            'is_cancel',
            'products',
            'total_price',
        )


class CreateOrderSerializer(serializers.ModelSerializer):
    # products = ProductInOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            # 'user',
            # 'create_date',
            # 'status',
            'payment',
            'delivery',
            # 'is_confirmed',
            # 'is_paid',
            # 'is_deliver',
            # 'is_completed',
            # 'is_cancel',
            # 'products',
            # 'total_price',
        )

    def create(self, validated_data):

        # get user basket
        try:
            basket = Basket.objects.get(user=self.context['request'].user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Basket_not_found")


        # if basket empty generate raise
        if not basket.total_price > 0:
            raise serializers.ValidationError("Basket_empty")

        # Create new order
        order = Order.objects.create(
            user=self.context['request'].user,
            payment=validated_data['payment'],
            delivery=validated_data['delivery'],
        )

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

