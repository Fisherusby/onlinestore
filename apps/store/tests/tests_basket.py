import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.orders.models import Basket, ProductInBasket
from apps.store.models import Brand, Category, OfferVendor, Product
from apps.users.models import CustomUser, UserProfile
from apps.vendors.models import Vendor


class ToBasketUserAPITestCase(APITestCase):
    def setUp(self):
        self.user_1 = CustomUser.objects.create(username='user 1')
        self.user_2 = CustomUser.objects.create(username='user 2')
        self.user_profile = UserProfile.objects.create(user=self.user_1, is_client=True, money_in_wallet=10000)
        self.basket_user = Basket.objects.create(user=self.user_1)
        self.client.force_login(self.user_1)
        self.brand_1 = Brand.objects.create(name='Brand 1')
        self.vendor_1 = Vendor.objects.create(name='Vendor 1', email='test@test.com', address='test st 32')
        self.category_1 = Category.objects.create(name='Category 1')
        self.product_1 = Product.objects.create(
            category=self.category_1,
            brand=self.brand_1,
            model='Model 1',
        )

        self.offer_1 = OfferVendor.objects.create(product=self.product_1, vendor=self.vendor_1, price=100)
        self.pib = ProductInBasket.objects.create(basket=self.basket_user, offer=self.offer_1, count=5)

        self.data = {'product': self.product_1.slug, 'vendor': self.vendor_1.slug}
        self.to_basket_url = reverse('ProductToBasketViewSet-list')

    def test_add_to_bad_offer_basket(self):
        response = self.client.post(
            self.to_basket_url,
            data=json.dumps(self.data),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_to_basket(self):
        self.offer_1 = OfferVendor.objects.create(product=self.product_1, vendor=self.vendor_1, price=100)
        response = self.client.post(
            self.to_basket_url,
            data=json.dumps(self.data),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_more_to_basket(self):
        response = self.client.post(
            self.to_basket_url,
            data=json.dumps(self.data),
            content_type='application/json',
        )
        pid_2 = ProductInBasket.objects.get(pk=self.pib.id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(pid_2.count, 6)

    def test_delete_from_bad_pib_basket(self):
        response = self.client.delete(reverse('ProductToBasketViewSet-detail', args=[50]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_from_basket(self):
        response = self.client.delete(reverse('ProductToBasketViewSet-detail', args=[self.pib.id]))
        pid_2 = ProductInBasket.objects.get(pk=self.pib.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(pid_2.count, 4)

    def test_delete_from_basket_zero_count(self):
        response = self.client.delete(reverse('ProductToBasketViewSet-detail', args=[self.pib.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_from_basket_not_owner(self):
        self.client.force_login(self.user_2)
        response = self.client.delete(reverse('ProductToBasketViewSet-detail', args=[self.pib.id]))
        pid_2 = ProductInBasket.objects.get(pk=self.pib.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(pid_2.count, 5)
