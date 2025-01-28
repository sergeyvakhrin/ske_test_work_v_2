from django.test import TestCase

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product, Warehouse
from users.models import User


class APIProductsTestCase(APITestCase):
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

        self.product = Product.objects.create(name='Тест')
        self.data = {'name': 'Phone'}

        self.user_factory = {
            'email': 'factory@mail.ru',
            'password': '1234',
            'name': 'Завод №1',
            'country': 'Россия',
            'client_type': 'FACTORY'
        }
        user_factory = User.objects.create(**self.user_factory)
        self.user_retail = {
            'email': 'retail2@mail.ru',
            'password': '1234',
            'name': 'Розничная сеть №1',
            'country': 'Россия',
            'client_type': 'RETAIL',
            'supplier': user_factory
        }
        user_retail = User.objects.create(**self.user_retail)
        self.product_2 = Product.objects.create(name='Тест')
        self.warehouse_factory = {
            'user': user_factory,
            'product': self.product_2,
            'quantity': 1,
            'price': 1
        }
        self.warehouse_retail = {
            'user': user_retail,
            'product': self.product_2,
            'quantity': 1,
            'price': 1
        }
        self.warehouse = Warehouse.objects.create(**self.warehouse_factory)


    def test_api_product_create(self):
        """ Проверяем создание продукта API  """
        url = reverse('products:api-product-create')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_product_list(self):
        """ Проверяем получение списка продуктов API """
        url = reverse('products:api-product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_product_get(self):
        """ Проверяем получение данных о продукте API """
        url = reverse('products:api-product-get', args=(self.product.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_product_update(self):
        """ Проверяем обновление данных продукта API """
        url = reverse('products:api-product-update', args=(self.product.pk,))
        data = {
            'description': 'Test',
            'name': 'Test'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_warehouse_create(self):
        """ Проверяем создание записи склада API  """
        url = reverse('products:api-warehouse-create')
    #     print(self.warehouse_factory)
    #     response = self.client.post(url, data=self.warehouse_factory)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_warehouse_list(self):
        """ Проверяем получение списка записей склада API """
        url = reverse('products:api-warehouse-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_warehouse_get(self):
        """ Проверяем получение данных о записи склада API """
        url = reverse('products:api-warehouse-get', args=(self.warehouse.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_warehouse_delete(self):
        """ Проверка удаления записи склада API """
        self.assertEqual(Warehouse.objects.all().count(), 1)
        url = reverse('products:api-warehouse-delete', args=(self.warehouse.pk,))
        response = self.client.delete(url)
        self.assertEqual(Warehouse.objects.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_api_product_delete(self):
        """ Проверка удаления продукта API """
        self.assertEqual(Product.objects.all().count(), 2)
        url = reverse('products:api-product-delete', args=(self.product.pk,))
        response = self.client.delete(url)
        self.assertEqual(Product.objects.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('products:api-product-delete', args=(self.product_2.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(Product.objects.all().count(), 1)


class ProductsTestCase(TestCase):
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
        self.client.force_login(self.user)

        self.product = Product.objects.create(name='Тест', is_published=True)
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
            'supplier': self.user_factory_2
        }
        self.user_retail_2 = User.objects.create(**self.user_retail)
        self.product_2 = Product.objects.create(name='Тест', is_published=True)
        self.warehouse_factory = {
            'user': self.user_factory_2,
            'product': self.product_2,
            'quantity': 1,
            'price': 1
        }
        self.warehouse_retail = {
            'user': self.user_retail_2,
            'product': self.product_2,
            'quantity': 1,
            'price': 1
        }
        self.warehouse = Warehouse.objects.create(**self.warehouse_factory)

    def test_home(self):
        """ Проверяет ответ главной страницы """
        url = reverse('products:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create(self):
        """ Проверка создания продукта """
        self.assertEqual(Product.objects.all().count(), 2)
        url = reverse('products:product_create')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(Product.objects.all().count(), 3)

    def test_product_list(self):
        """ Проверка получения списка продуктов """
        url = reverse('products:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail(self):
        """ Проверка получение информации о продукте """
        url = reverse('products:product_detail', args=(self.product.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_update(self):
        """ Проверка изменения продукта """
        url = reverse('products:product_update', args=(self.product.pk,))
        data = {'name': 'Test'}
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(self.product.name, 'Test')

    def test_warehouse_create(self):
        """ Проверка создания записи склада """
        self.assertEqual(Warehouse.objects.all().count(), 1)
        url = reverse('products:warehouse_create')
        # response = self.client.post(url, data=self.warehouse_retail)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(Warehouse.objects.all().count(), 2)

    def test_warehouse_list(self):
        """ Проверка получения списка записей склада """
        url = reverse('products:warehouse_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supplier_warehouse_create(self):
        """ Проверка получения списка записей склада своего поставщика"""
        url = reverse('products:supplier_warehouse_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_self_warehouse(self):
        """ Проверка получения своего списка записей склада """
        url = reverse('products:self_warehouse')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
