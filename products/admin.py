from django.contrib import admin
from django.utils.safestring import mark_safe

from products.models import Product, Warehouse
from users.models import User


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Выводим в админ панель таблицу индивидуальных предпринимателей """
    list_display = ['id', 'name', 'model_product', 'description', 'prod_photo', 'is_published', 'release_date']
    list_display_links = ['id', 'name', 'model_product', 'description', 'is_published', 'release_date']

    def get_readonly_fields(self, request, obj=None):
        """ Делаем поля только для чтения, если просмотр """
        if obj:
            return self.readonly_fields + ('id', 'release_date')
        return self.readonly_fields

    @admin.display(description='Изображение')
    def prod_photo(self, product: Product):
        """ Отображение фото в админке """
        # TODO: картинка не отображается
        if product.photo:
            return mark_safe(f"<img src='{product.photo.url}' width=50>")
        return "Без фото"


@admin.register(Warehouse)
class ProductAdmin(admin.ModelAdmin):
    """ Выводим в админ панель таблицу индивидуальных предпринимателей """
    list_display = ['id', 'user_name', 'user_email', 'product', 'product_model', 'product_description', 'prod_photo', 'quantity', 'price']
    list_display_links =['id', 'user_name', 'user_email', 'product', 'quantity', 'price']

    @admin.display(description='Модель')
    def product_model(self, warehouse: Warehouse):
        """ Выводим модель товара """
        return warehouse.product.model_product

    @admin.display(description='Описание')
    def product_description(self, warehouse: Warehouse):
        """ Выводим описание товара """
        return warehouse.product.description

    @admin.display(description='Название Организации')
    def user_name(self, user: User):
        """ Выводим наименование Организации """
        return user.user.name

    @admin.display(description='Электронная почта')
    def user_email(self, user: User):
        """ Выводим почту Организации """
        return user.user.email

    def get_readonly_fields(self, request, obj=None):
        """ Делаем поля только для чтения, если просмотр """
        if obj:
            return self.readonly_fields + ('user', 'product', 'quantity', 'price')
        return self.readonly_fields

    @admin.display(description='Изображение')
    def prod_photo(self, warehouse: Warehouse):
        """ Отображение фото в админке """
        # TODO: картинка не отображается
        if warehouse.product.photo:
            return mark_safe(f"<img src='{warehouse.product.photo.url}' width=50>")
        return "Без фото"
