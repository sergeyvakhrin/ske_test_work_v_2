from django import forms
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm
from django.forms import ModelForm

from users.models import User


class UserRegisterForm(ModelForm):
    """ Класс создания формы пользователя """
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'country', 'city', 'street', 'house_number', 'client_type', 'supplier']

    def __init__(self, *args, **kwargs):
        """ Меняем password на Пароль """
        super().__init__(*args, **kwargs)
        self.fields['password'].label = 'Пароль'


class UserDebtNullForm(ModelForm):
    """ Класс редактирования данных пользователей с долгом """
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'country', 'city', 'street', 'house_number', 'client_type', 'supplier', 'debt']

    def __init__(self, *args, **kwargs):
        """ Меняем password на Пароль """
        super().__init__(*args, **kwargs)
        self.fields['password'].label = 'Пароль'


class UserProfileForm(UserChangeForm):
    """ Класс создания формы для просмотра деталей профиля пользователя """
    extra_created_at = forms.DateField(required=True, label='Дата образования:', disabled=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'country', 'city', 'street', 'house_number', 'client_type', 'extra_created_at', 'supplier', 'debt']

    def __init__(self, *args, **kwargs):
        """
        Вводим ограничения на редактирование полей:
        password Что бы скрыть в форме "Пароль не задан"
        """
        super().__init__(*args, **kwargs)
        user = kwargs.get('instance')

        self.fields['password'].widget = forms.HiddenInput()
        self.fields['debt'].disabled = True
        self.fields['client_type'].disabled = True
        self.initial['extra_created_at'] = user.created_at

        if user.groups.filter(name='Moderators').exists():
            self.fields['password'].widget = forms.HiddenInput()
            self.fields['debt'].widget = forms.HiddenInput()
            self.fields['client_type'].widget = forms.HiddenInput()
            self.fields['supplier'].widget = forms.HiddenInput()
            self.fields['name'].widget = forms.HiddenInput()
        else:
            user_supplier = user.supplier
            if user.client_type == "FACTORY":
                self.fields['supplier'].widget = forms.HiddenInput()
                self.fields['debt'].widget = forms.HiddenInput()
            else:
                if user_supplier is not None:
                    self.fields['supplier'].disabled = True


class MyAuthenticationForm(AuthenticationForm):
    """ Все ради слова Пароль при авторизации """

    def __init__(self, *args, **kwargs):
        """ Меняем password на Пароль """
        super().__init__(*args, **kwargs)
        self.fields['password'].label = 'Пароль'