from django.shortcuts import render
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from products.models import Warehouse
from users.models import User
from users.serializers import UserSerializer, UserSerializerWithoutDebtField


class UserCreateAPIView(CreateAPIView):
    """ Контроллер создания пользователя """
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        """  """
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """ Контроллер просмотра списка пользователей """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserRetrieveAPIView(RetrieveAPIView):
    """ Контроллер получение отдельного пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserUpdateAPIView(UpdateAPIView):
    """ Контроллер изменения данных Пользователей """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        """Выбираем сериалайзер, для исключить редактирования полей client_type, debt, supplier для Update """
        serializer_class = self.serializer_class
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = UserSerializerWithoutDebtField
        return serializer_class


class UserDeleteAPIView(DestroyAPIView):
    """ Контроллер удаления пользователей """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def delete(self, request, *args, **kwargs):
        """ Проверяем наличие покупателей и товаров на складе """
        user = User.objects.get(pk=self.kwargs.get('pk'))
        warehouse = Warehouse.objects.filter(user=user)
        if warehouse:
            raise APIException('Нельзя удалить организацию. Сначала переместите товар на другой склад.')
        if user.user_supplier:
            supplier = User.objects.get(pk=user.supplier_id)
            User.objects.filter(supplier=user).update(supplier=supplier)

            # raise APIException('Сначала перенаправьте покупателей.')

        return self.destroy(request, *args, **kwargs)