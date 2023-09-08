from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import CustomUser


class RegisterAPITestCase(APITestCase):
    def setUp(self):
        self.superuser = CustomUser.objects.create_superuser('admit', 'admit@example.com', 'johnpassword')
        self.user = CustomUser.objects.create(username='user')
        self.client.login(username='john', password='johnpassword')
        self.user_data = {
            'username': 'new_user',
            'first_name': 'new_user',
            'last_name': 'new_user',
            'password': 'johnpassword',
            'email': 'new_user@example.com',
        }
        self.register_url = reverse('RegisterClientUserViewSet-list')

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_users(self):
        response = self.client.get(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_register_user_auth_admit(self):
        self.client.force_login(self.superuser)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_auth(self):
        self.client.force_login(self.user)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


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
