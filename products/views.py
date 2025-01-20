from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer


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
