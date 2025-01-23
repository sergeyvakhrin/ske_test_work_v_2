from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {"null": True, "blank": True}

class User(AbstractUser):
    """ Модель для авторизации """
    CHOICES = {
        "FACTORY": "Завод",
        "RETAIL": "Розничная сеть",
        "INDIVIDUAL": "Индивидуальный предприниматель"
    }
    username = None

    email = models.EmailField(max_length=255, unique=True, verbose_name='Почта')
    name = models.CharField(max_length=255, verbose_name='Наименование организации', unique=True)
    country = models.CharField(max_length=30, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город', **NULLABLE)
    street = models.CharField(max_length=100, verbose_name='Улица', **NULLABLE)
    house_number = models.CharField(max_length=10, verbose_name='Номер дома', **NULLABLE)
    client_type = models.CharField(max_length=100, choices=CHOICES, verbose_name='Тип клиента')
    # product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name='Продукты', **NULLABLE)
    created_at = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Поставщик', **NULLABLE, related_name='user_supplier')
    debt = models.FloatField(default=0, verbose_name='Задолженность перед поставщиком')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name
