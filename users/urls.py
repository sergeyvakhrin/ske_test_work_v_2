from django.urls import path
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDeleteAPIView, \
    RegisterView, logout_view, UserProfileView, UserDetailView, MyLoginView, UserListView, UserUpdateView, \
    ProductDebtNullUpdateView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("api/register/", UserCreateAPIView.as_view(), name="api_register"),
    path("api/login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="api_login"),
    path("api/token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),

    path("api/list/", UserListAPIView.as_view(), name='api-user-list'),
    path("api/<int:pk>/", UserRetrieveAPIView.as_view(), name="api-user-get"),
    path("api/update/<int:pk>/", UserUpdateAPIView.as_view(), name="api-user-update"),
    path("api/delete/<int:pk>/", UserDeleteAPIView.as_view(), name="api-user-delete"),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/<int:pk>/view', UserDetailView.as_view(), name='user_detail'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/update', UserUpdateView.as_view(), name='user_update'),
    path('product/debt/null/<int:pk>/', ProductDebtNullUpdateView.as_view(), name='user_update_debt_null'),
]
