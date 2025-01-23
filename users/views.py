from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from products.models import Warehouse
from users.forms import UserRegisterForm, UserProfileForm, MyAuthenticationForm
from users.models import User
from users.serializers import UserSerializer, UserSerializerWithoutDebtField
from users.servises import IsOwner, IsModer, UsersCustomPagination


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
    pagination_class = UsersCustomPagination
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


class MyLoginView(LoginView):
    """ Все ради слова Пароль при авторизации """
    form_class = MyAuthenticationForm


def logout_view(request):
    """ Функция для кастомного выходы из сервиса """
    logout(request)
    return redirect('/')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.set_password(user.password)
        user.save()
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, UpdateView):
    """ Класс для просмотра и редактирования профиля пользователя """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(DetailView):
    """ Контроллер для отображения данных поставщика """
    model = User

