from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from products.models import Product, Warehouse
from products.serializers import ProductSerializer, WarehouseSerializer
from products.servises import ProductsCustomPagination, IsModer, IsOwner


class ProductCreateAPIView(CreateAPIView):
    """ Контроллер создания номенклатуры продуктов. """
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )


class ProductListAPIView(ListAPIView):
    """ Контроллер вывода номенклатуры продуктов """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated, )
    pagination_class = ProductsCustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'model_product', 'description']
    filterset_fields = ('name', 'model_product', 'description',)


class ProductRetrieveAPIView(RetrieveAPIView):
    """ Контроллер получение отдельного продукта """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated, )


class ProductUpdateAPIView(UpdateAPIView):
    """ Контроллер изменения продукта """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated, )


class ProductDeleteAPIView(DestroyAPIView):
    """ Контроллер удаления продуктов """
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated, IsModer, )

    def perform_destroy(self, instance):
        """ Делаем продукты не опубликованными """
        if instance:
            if Warehouse.objects.filter(product=instance).exists():
                instance.is_published = False
                instance.save()
                raise APIException('Нельзя удалить товар, если он находится на складе у клиента. Товар убран из продажи')
            instance.delete()


class WarehouseCreateAPIView(CreateAPIView):
    """ Контроллер создания операции по складу """
    serializer_class = WarehouseSerializer
    permission_classes = (AllowAny,)


class WarehouseListAPIView(ListAPIView):
    """ Контроллер просмотра списка операции по складу """
    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects.all()
    permission_classes = (IsModer,)
    pagination_class = ProductsCustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['product']
    filterset_fields = ('product',)


class WarehouseRetrieveAPIView(RetrieveAPIView):
    """ Контроллер получение отдельной операции по складу """
    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | IsModer)


class WarehouseDeleteAPIView(DestroyAPIView):
    """ Контроллер удаления операции по складу """
    queryset = Warehouse.objects.all()
    permission_classes = (IsModer,)

    def perform_destroy(self, instance):
        """ Запрещаем удаление операций по складу """
        if instance:
            raise APIException('Нельзя удалять операции по складу без соответствующих документов!')


def home(request):
    """ Контроллер стартовой страницы """
    context = {}
    return render(request, 'products/home.html', context)
