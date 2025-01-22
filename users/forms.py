from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm

from users.models import User


class UserRegisterForm(ModelForm):
    """ Класс создания формы ввода номера телефона """
    class Meta:
        model = User
        fields = '__all__'


class UserProfileForm(UserChangeForm):
    """ Класс создания формы для просмотра деталей профиля пользователя """
    class Meta:
        model = User
        fields = '__all__'



