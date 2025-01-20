from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from products.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDeleteAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="api_register"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),

    path("user/list/", UserListAPIView.as_view(), name='api-user-list'),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="api-user-get"),
    path("user/update/<int:pk>/", UserUpdateAPIView.as_view(), name="api-user-update"),
    path("user/delete/<int:pk>/", UserDeleteAPIView.as_view(), name="api-user-delete"),
]
