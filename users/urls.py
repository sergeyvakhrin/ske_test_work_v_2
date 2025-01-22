from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDeleteAPIView, \
    ProductCreateAPIView, ProductListAPIView, ProductRetrieveAPIView, ProductUpdateAPIView, ProductDeleteAPIView, \
    WarehouseCreateAPIView, WarehouseListAPIView, WarehouseRetrieveAPIView, WarehouseDeleteAPIView
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

    path("product/create/", ProductCreateAPIView.as_view(), name="api-product-create"),
    path("product/list/", ProductListAPIView.as_view(), name="api-product-list"),
    path("product/<int:pk>/", ProductRetrieveAPIView.as_view(), name="api-product-get"),
    path("product/update/<int:pk>/", ProductUpdateAPIView.as_view(), name="api-product-update"),
    path("product/delete/<int:pk>/", ProductDeleteAPIView.as_view(), name="api-product-delete"),

    path("warehouse/create/", WarehouseCreateAPIView.as_view(), name="api-warehouse-create"),
    path("warehouse/list/", WarehouseListAPIView.as_view(), name="api-warehouse-list"),
    path("warehouse/<int:pk>/", WarehouseRetrieveAPIView.as_view(), name="api-warehouse-get"),
    path("warehouse/delete/<int:pk>/", WarehouseDeleteAPIView.as_view(), name="api-warehouse-delete"),
]
