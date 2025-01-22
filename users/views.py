from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from products.models import Warehouse, Product
from products.serializers import ProductSerializer
from users.models import User
from users.serializers import UserSerializer, UserSerializerWithoutDebtField
from users.servises import IsOwner, IsModer, CustomPagination


class UserCreateAPIView(CreateAPIView):
    """ Контроллер создания пользователя """
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        """ Хешируем пароль """
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """ Контроллер просмотра списка пользователей """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsModer,)
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['country']
    filterset_fields = ('country',)

class UserRetrieveAPIView(RetrieveAPIView):
    """ Контроллер получение отдельного пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | IsModer)


class UserUpdateAPIView(UpdateAPIView):
    """ Контроллер изменения данных Пользователей """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | IsModer)

    def get_serializer_class(self):
        """ Выбираем сериалайзер, что бы исключить из редактирования поля client_type, debt, supplier для Update """
        serializer_class = self.serializer_class
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = UserSerializerWithoutDebtField
        return serializer_class


class UserDeleteAPIView(DestroyAPIView):
    """ Контроллер удаления пользователей """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)

    def delete(self, request, *args, **kwargs):
        """
        Проверяем наличие покупателей и товаров на складе.
        Пере привязываем покупателе к предыдущему поставщику.
        """
        user = User.objects.get(pk=self.kwargs.get('pk'))
        warehouse = Warehouse.objects.filter(user=user)
        if warehouse:
            raise APIException('Нельзя удалить организацию. Сначала переместите товар на другой склад.')
        if user.user_supplier:
            supplier = User.objects.get(pk=user.supplier_id)
            User.objects.filter(supplier=user).update(supplier=supplier)

        return self.destroy(request, *args, **kwargs)


class ProductCreateAPIView(CreateAPIView):
    """ Контроллер создания номенклатуры продуктов. """
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )


class ProductListAPIView(ListAPIView):
    """ Контроллер вывода номенклатуры продуктов """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination
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
