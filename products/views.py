from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from products.forms import ProductCreateForm, FormWarehouse, FormWarehouseBuy
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
    permission_classes = (IsAuthenticated,)


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


class ProductCreateView(LoginRequiredMixin, CreateView):
    """ Контроллер создания продукта """
    model = Product
    form_class = ProductCreateForm
    template_name = 'products/product_register.html'
    success_url = reverse_lazy('products:product_list')


class ProductListView(ListView):
    """ Контроллер просмотра списка продуктов """
    model = Product


class ProductDetailView(LoginRequiredMixin, DetailView):
    """ Контроллер просмотра деталей продукты """
    model = Product


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """ Контроллер изменения продукта """
    model = Product
    form_class = ProductCreateForm
    success_url = reverse_lazy('products:product_list')


class WarehouseCreateView(LoginRequiredMixin, CreateView):
    """ Контроллер создания записи в складе """
    model = Warehouse
    form_class = FormWarehouse
    template_name = 'products/warehouse_register.html'
    success_url = reverse_lazy('products:warehouse_list')

    def get_form_kwargs(self):
        """ Получаем доступ к queryset для фильтрации
        https://medium.com/analytics-vidhya/django-how-to-pass-the-user-object-into-form-classes-ee322f02948c"""
        kwargs = super(WarehouseCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class WarehouseBuyCreateView(LoginRequiredMixin, CreateView):
    """ Контроллер создания записи в складе по кнопке Купить """
    model = Warehouse
    form_class = FormWarehouseBuy
    template_name = 'products/warehouse_register.html'
    success_url = reverse_lazy('products:warehouse_list')

    def get_form_kwargs(self):
        """ Получаем доступ к queryset для фильтрации
        https://medium.com/analytics-vidhya/django-how-to-pass-the-user-object-into-form-classes-ee322f02948c"""
        kwargs = super(WarehouseBuyCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


# class WarehouseListView(ListView):
#     """ Контроллер вывода записей склада """
#     model = Warehouse


class WarehouseSupplierListView(LoginRequiredMixin, ListView):
    """ Контроллер вывода остатков своего поставщика """
    model = Warehouse
    template_name = 'products/warehouse_sup_buy.html'

    def get_queryset(self):
        """ Получаем остаток склада поставщика """
        user = self.request.user
        if not user.is_staff or not user.is_superuser:
            supplier = user.supplier
            return Warehouse.objects.filter(user=supplier)
        return Warehouse.objects.all()


class WarehouseSelfListView(LoginRequiredMixin, ListView):
    """ контроллер остатков склада пользователя """
    model = Warehouse

    def get_queryset(self):
        """ Получаем остаток склада пользователя """
        user = self.request.user
        if not user.is_staff or not user.is_superuser:
            return Warehouse.objects.filter(user=user)
        return Warehouse.objects.all()
