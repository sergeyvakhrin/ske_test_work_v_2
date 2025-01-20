from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from products.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="api_register"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),

    path("list/", UserListAPIView.as_view(), name='api-list'),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="api-get"),
]
