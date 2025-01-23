from django.contrib.auth.views import LoginView
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDeleteAPIView, \
    RegisterView, logout_view, UserProfileView
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
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', UserProfileView.as_view(), name='profile'),
]
