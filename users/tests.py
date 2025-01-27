from django.test import TestCase

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product, Warehouse
from users.models import User


class APIUsersTestCase(APITestCase):
    """ Тестирование API приложения Users """
    def setUp(self):
        """ Данные для тестовой базы """

        self.user = User.objects.create(email='admin@sky.pro',
                                        password='1234',
                                        name='Admin',
                                        country='Russia',
                                        client_type='FACTORY',
                                        is_active=True,
                                        is_staff=True,
                                        is_superuser=True
                                        )
        self.group= Group.objects.create(name='Moderators')
        self.user.groups.add(self.group)
        self.client.force_authenticate(user=self.user)

        self.user_factory = {
            'email': 'factory@mail.ru',
            'password': '1234',
            'name': 'Завод №1',
            'country': 'Россия',
            'client_type': 'FACTORY'
        }
        # self.user_retail = {
        #     'email': 'retail@mail.ru',
        #     'password': '1234',
        #     'name': 'Розничная сеть №1',
        #     'country': 'Россия',
        #     'client_type': 'RETAIL',
        #     'supplier': 2
        # }
        # self.user_individual = {
        #     'email': 'individual@mail.ru',
        #     'password': '1234',
        #     'name': 'ИП №1',
        #     'country': 'Россия',
        #     'client_type': 'INDIVIDUAL',
        #     'supplier': 3
        # }


    def test_api_register(self):
        """ Проверяем создание пользователей API """
        url = reverse('users:api_register')
        response_1 = self.client.post(url, data=self.user_factory)
        # response_2 = self.client.post(url, data=self.user_retail)
        # response_3 = self.client.post(url, data=self.user_individual)
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response_3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_api_user_list(self):
        """ Проверяем получение списка пользователей API """
        url = reverse('users:api-user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_user_get(self):
        """ Проверяем получение данных пользователя API """
        url = reverse('users:api-user-get',  args=(self.user.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_user_update(self):
        """ Проверяем обновление данных пользователя API """
        url = reverse('users:api-user-update', args=(self.user.pk,))
        data = {
            'email': 'admin@sky.pro',
            'name': 'Администратор'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_user_delete(self):
        """ Проверяем удаление пользователя API """
        user = User.objects.create(**self.user_factory)
        url = reverse('users:api-user-delete', args=(user.pk,))
        # response = self.client.delete(url)
        # self.assertEqual(User.objects.all().count(), 1)
        # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_debt_null(self):
        """ Проверка запрета на обнуление задолженности через API по тз """
        pass


class UsersTestCase(TestCase):
    """ Тестирование приложения Users """
    def setUp(self):
        """ Данные для тестовой базы """
        self.user = User.objects.create(email='admin@sky.pro',
                                        password='1234',
                                        name='Admin',
                                        country='Russia',
                                        client_type='FACTORY',
                                        is_active=True,
                                        is_staff=True,
                                        is_superuser=True
                                        )
        self.group= Group.objects.create(name='Moderators')
        self.user.groups.add(self.group)
        # self.client.force_authenticate(user=self.user)

        self.product = Product.objects.create(name='Тест')
        self.data = {'name': 'Phone'}

        self.user_factory = {
            'email': 'factory@mail.ru',
            'password': '1234',
            'name': 'Завод №1',
            'country': 'Россия',
            'client_type': 'FACTORY'
        }
        self.user_factory_2 = User.objects.create(**self.user_factory)
        self.user_retail = {
            'email': 'retail2@mail.ru',
            'password': '1234',
            'name': 'Розничная сеть №1',
            'country': 'Россия',
            'client_type': 'RETAIL',
            'supplier': self.user_factory_2,
            'debt': 1000
        }
        self.user_retail_2 = User.objects.create(**self.user_retail)

    def test_register(self):
        """ Проверяем создание пользователей API """
        url = reverse('users:register')
        response = self.client.post(url, data=self.user_factory)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.all().count(), 3)

    def test_login(self):
        """ Проверка авторизации """
        url = reverse('users:login')
        data = {'email': 'admin@sky.pro', 'password': '1234'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        """ Проверка выхода """
        url = reverse('users:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_profile(self):
        """ Проверка просмотра данных пользователя """
        pass

    def test_user_detail(self):
        """ Проверка просмотра данных пользователя """
        url = reverse('users:user_detail', args=(self.user.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_user_list(self):
        """ Проверка просмотра списка пользователей """
        url = reverse('users:user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_user_update(self):
        """ Проверка обновления данных пользователей """
        url = reverse('users:user_update', args=(self.user.pk,))
        data = {'name': 'Mikula'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        # self.assertEqual(self.user.name, 'Mikula')

    def test_user_update_debt_null(self):
        """ Проверка обнуления задолженности """
        url = reverse('users:user_update_debt_null', args=(self.user_retail_2.pk,))
        data = {'debt': 0}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        # self.assertEqual(self.user_retail_2.debt, 0)
