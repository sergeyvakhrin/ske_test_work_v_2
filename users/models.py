from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings

NULLABLE = {"null": True, "blank": True}

class User(AbstractUser):
    """ Модель для авторизации """
    CHOICES = {
        "FACTORY": "Factory",
        "RETAIL": "Retail",
        "INDIVIDUAL": "Individual entrepreneur"
    }
    username = None

    email = models.EmailField(max_length=255, unique=True, verbose_name='Почта', help_text='Укажите почту')
    name = models.CharField(max_length=255, verbose_name='Наименование организации', help_text='Укажите наименование организации', unique=True)
    country = models.CharField(max_length=30, verbose_name='Страна', help_text='Укажите страну производства')
    city = models.CharField(max_length=100, verbose_name='Город', help_text='Укажите город', **NULLABLE)
    street = models.CharField(max_length=100, verbose_name='Улица', help_text='Укажите улицу', **NULLABLE)
    house_number = models.CharField(max_length=10, verbose_name='Номер дома', help_text='Укажите номер дома', **NULLABLE)
    client_type = models.CharField(max_length=100, choices=CHOICES, unique=True, verbose_name='Тип клиента',                                   help_text='Укажите тип клиента')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', help_text='Выберите пользователя', related_name='user_retail')
    # product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name='Продукты', **NULLABLE)
    created_at = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Поставщик', help_text='Укажите поставщика', **NULLABLE, related_name='user_supplier')
    debt = models.FloatField(default=0, verbose_name='Задолженность перед поставщиком')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
