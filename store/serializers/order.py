from rest_framework import serializers
from store.models import Order, ProductInOrder, Basket, ProductInBasket, ReceiptOfPayment
from tools.notify import notify_order
from django.core.exceptions import ObjectDoesNotExist

from users.models import UserProfile


class ProductInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInOrder
        fields = (
            'product',
            'vendor',
            'price_in_currency',
            'price_count',
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
            'payment',
            'receipts',
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

        if basket.total_price.get('BYN', 0) == 0:
            raise serializers.ValidationError("Basket_empty")

        # Create new order
        order = Order.objects.create(
            user=self.context['request'].user,
            payment=validated_data['payment'],
            delivery=validated_data['delivery'],
        )

        # Add goods in order from basket
        for gib in basket.products_in_basket.all():
            ProductInOrder.objects.create(
                order=order,
                product=gib.product,
                vendor=gib.offer.vendor,
                price=gib.offer.price,
                count=gib.count,
            )

        # clear basket
        # ProductInBasket.objects.filter(basket=basket).delete()

        # send email to user about order
        order_send = Order.objects.get(id=order.id)
        notify_order(order_send)

        return order


class PayOrderByWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptOfPayment
        fields = (
            'order',
            'method',
        )

    def create(self, validated_data):
        if validated_data['method'] != 'wallet':
            raise serializers.ValidationError("payment_method_error")
        try:

            order = Order.objects.get(id=validated_data['order'].id, user=self.context['request'].user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Order_not_found")

        if order.total_price.get('BYN', 0) == 0:
            raise serializers.ValidationError("Order_empty")

        try:
            if self.context['request'].user.user_profile.money_in_wallet < order.total_price['BYN']:
                raise serializers.ValidationError("Not_enough_money")
            else:
                receipt = ReceiptOfPayment.objects.create(order=order, method='wallet', price=order.total_price['BYN'])
                self.context['request'].user.user_profile.money_in_wallet -= order.total_price['BYN']
                self.context['request'].user.save()
                order.is_paid = True
                order.status = 'delivery'
                order.save()
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("Not_enough_wallet")

        return receipt



class PayOrderByCardtSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptOfPayment
        fields = (
            'order',
            'method',
            'card',

        )

    def create(self, validated_data):
        import braintree
        from django.conf import settings

        gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

        if validated_data['method'] != 'online':
            raise serializers.ValidationError("payment_method_error")
        try:
            order = Order.objects.get(id=validated_data['order'].id, user=self.context['request'].user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Order_not_found")

        if order.total_price.get('BYN', 0) == 0:
            raise serializers.ValidationError("Order_empty")


        try:
            if self.context['request'].user.user_profile.money_in_wallet < order.total_price['BYN']:
                raise serializers.ValidationError("Not_enough_money")
            else:
                receipt = ReceiptOfPayment.objects.create(order=order, method='wallet', price=order.total_price['BYN'])
                self.context['request'].user.user_profile.money_in_wallet -= order.total_price['BYN']
                self.context['request'].user.save()
                order.is_paid = True
                order.status = 'delivery'
                order.save()
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("Not_enough_wallet")

        return receipt
