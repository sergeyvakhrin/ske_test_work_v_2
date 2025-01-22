from django.contrib.auth.views import LoginView
from django.urls import path

from products.apps import ProductsConfig
from products.views import home, logout_view, UserProfileView, RegisterView

app_name = ProductsConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='products/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', UserProfileView.as_view(), name='profile'),

]
