from django.db import models

from users.models import User

NULLABLE = {"null": True, "blank": True}

class Product(models.Model):
    """ Модель для таблицы Продуктов """
    name = models.CharField(max_length=255, verbose_name='Название', help_text='Укажите название продукта', )
    model_product = models.CharField(max_length=255, verbose_name='Модель', help_text='Укажите модель продукта', **NULLABLE)
    description = models.TextField(verbose_name='Описание', help_text='Добавьте описание продукта', **NULLABLE)
    photo = models.ImageField(upload_to="products/photo/", verbose_name="Фото", **NULLABLE, help_text="Загрузите фото")
    is_published = models.BooleanField(verbose_name='В продаже', help_text='Отметьте если в продаже', default=True)
    release_date = models.DateField(verbose_name='Дата выхода', help_text='Укажите дату выхода на рынок', **NULLABLE)

    # TODO: Добавлять продукты могут только заводы. Сделать выборку в поле user

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    """ Модель для таблицы Склад """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Организация', related_name='user_warehouse')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Продукты', related_name='product_warehouse')
    quantity = models.PositiveIntegerField(verbose_name='Количество', help_text='Укажите доступное количество', default=0)
    price = models.FloatField(verbose_name='Цена', help_text='Укажите стоимость', default=0)

    class Meta:
        verbose_name = 'Продукт на склад'
        verbose_name_plural = 'Продукты на Складах'

    def __str__(self):
        return self.user.name
