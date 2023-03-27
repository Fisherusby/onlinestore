from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.store.models import Brand, Vendor, Category, Product, OfferVendor, Basket, ProductInBasket
from apps.users.models import UserProfile, CustomUser
import json


class ToBasketUserAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='john')
        self.user_2 = CustomUser.objects.create(username='john 2')
        self.user_profile = UserProfile.objects.create(user=self.user, is_client=True, money_in_wallet=10000)
        self.basket_user = Basket.objects.create(user=self.user)
        self.client.force_login(self.user)
        self.brand_1 = Brand.objects.create(name='Brand 1')
        self.vendor_1 = Vendor.objects.create(name='Vendor 1', email='test@test.com', address='test st 32')
        self.category_1 = Category.objects.create(name='Category 1')
        self.product_1 = Product.objects.create(
            category=self.category_1,
            brand=self.brand_1,
            model='Model 1',
        )
        self.data = {'product': self.product_1.slug, 'vendor': self.vendor_1.slug}

    def test_add_to_bad_offer_basket(self):
        response = self.client.post(reverse('ProductToBasketViewSet-list'), data=json.dumps(self.data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_to_basket(self):
        self.offer_1 = OfferVendor.objects.create(product=self.product_1, vendor=self.vendor_1, price=100)
        response = self.client.post(reverse('ProductToBasketViewSet-list'), data=json.dumps(self.data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_more_to_basket(self):
        self.offer_1 = OfferVendor.objects.create(product=self.product_1, vendor=self.vendor_1, price=100)
        self.pib = ProductInBasket.objects.create(basket=self.basket_user, offer=self.offer_1, count=5)

        response = self.client.post(reverse('ProductToBasketViewSet-list'), data=json.dumps(self.data),
                                    content_type='application/json')
        self.pid_2 = ProductInBasket.objects.get(pk=self.pib.id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.pid_2.count, 6)

    def test_delete_from_bad_pib_basket(self):
        response = self.client.delete(reverse('ProductToBasketViewSet-detail', args=[50]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_from_basket(self):
        self.offer_1 = OfferVendor.objects.create(product=self.product_1, vendor=self.vendor_1, price=100)
        self.pib = ProductInBasket.objects.create(basket=self.basket_user, offer=self.offer_1, count=5)
        response = self.client.delete(reverse('ProductToBasketViewSet-detail', args=[self.pib.id]))
        self.pid_2 = ProductInBasket.objects.get(pk=self.pib.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.pid_2.count, 4)

    def test_delete_from_basket_zero_count(self):
        self.offer_1 = OfferVendor.objects.create(product=self.product_1, vendor=self.vendor_1, price=100)
        self.pib = ProductInBasket.objects.create(basket=self.basket_user, offer=self.offer_1, count=0)
        response = self.client.delete(reverse('ProductToBasketViewSet-detail', args=[self.pib.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_from_basket_not_owner(self):
        self.offer_1 = OfferVendor.objects.create(product=self.product_1, vendor=self.vendor_1, price=100)
        self.pib = ProductInBasket.objects.create(basket=self.basket_user, offer=self.offer_1, count=5)
        self.client.force_login(self.user_2)
        response = self.client.delete(reverse('ProductToBasketViewSet-detail', args=[self.pib.id]))
        self.pid_2 = ProductInBasket.objects.get(pk=self.pib.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.pid_2.count, 5)

    # def add_to_basket(self):
    #     response = self.client.post(reverse('ProductToBasketViewSet-list'), self.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)






# class RegisterAuthAdminUserAPITestCase(APITestCase):
#     def setUp(self):
#         self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
#         self.client.login(username='john', password='johnpassword')
#         self.data = {'username': 'mike', 'first_name': 'Mike', 'last_name': 'Tyson', 'password': 'johnpassword', 'email': 'john@snow.com'}
#
#     def test_can_register_user(self):
#         response = self.client.post(reverse('RegisterClientUserViewSet-list'), self.data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#
# class RegisterAuthNonAdminUserAPITestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create(username='john')
#         self.client.force_login(self.user)
#         self.data = {'username': 'mike', 'first_name': 'Mike', 'last_name': 'Tyson', 'password': 'johnpassword', 'email': 'john@snow.com'}
#
#     def test_can_register_user(self):
#         response = self.client.post(reverse('RegisterClientUserViewSet-list'), self.data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# class ReadUserTest(APITestCase):
#     def setUp(self):
#         self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
#         self.client.login(username='john', password='johnpassword')
#         self.user = User.objects.create(username="mike")
#
#     def test_can_read_user_list(self):
#         response = self.client.get(reverse('user-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_can_read_user_detail(self):
#         response = self.client.get(reverse('user-detail', args=[self.user.id]))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class UpdateUserTest(APITestCase):
#     def setUp(self):
#         self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
#         self.client.login(username='john', password='johnpassword')
#         self.user = User.objects.create(username="mike", first_name="Tyson")
#         self.data = RegisterUserSerializer(self.user).data
#         self.data.update({'first_name': 'Changed'})
#
#     def test_can_update_user(self):
#         response = self.client.put(reverse('user-detail', args=[self.user.id]), self.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class DeleteUserTest(APITestCase):
#     def setUp(self):
#         self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
#         self.client.login(username='john', password='johnpassword')
#         self.user = User.objects.create(username="mikey")
#
#     def test_can_delete_user(self):
#         response = self.client.delete(reverse('user-detail', args=[self.user.id]))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#