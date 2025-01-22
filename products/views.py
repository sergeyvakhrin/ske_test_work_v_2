from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from users.forms import UserProfileForm, UserRegisterForm
from users.models import User


def home(request):
    """ Контроллер стартовой страницы """
    context = {}
    return render(request, 'products/home.html', context)

def logout_view(request):
    """ Функция для кастомного выходы из сервиса """
    logout(request)
    return redirect('/')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class UserProfileView(LoginRequiredMixin, UpdateView):
    """ Класс для просмотра и редактирования профиля пользователя """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('products:profile')

    def get_object(self, queryset=None):
        return self.request.user

