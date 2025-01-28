from django.contrib import admin
from django.utils.safestring import mark_safe

from products.forms import FormWarehouse, AdminFormWarehouse
from products.models import Product, Warehouse
from users.models import User


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Выводим в админ панель таблицу номенклатуры продуктов """
    list_display = ['id', 'name', 'model_product', 'description', 'prod_photo', 'is_published', 'release_date']
    list_display_links = ['id', 'name', 'model_product', 'description', 'prod_photo', 'is_published', 'release_date']
    search_fields = ['name', 'model_product', 'description', 'is_published', 'release_date']
    list_filter = ['name', 'model_product', 'description', 'is_published', 'release_date']
    save_on_top = True

    def delete_queryset(self, request, queryset):
        """ Делаем товар не активным при попытке его удаления """
        queryset.update(is_published=False)

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
class WarehouseAdmin(admin.ModelAdmin):
    """ Выводим в админ панель таблицу товары на складе конкретного пользователя """
    form = AdminFormWarehouse
    fields = ['user', 'product', 'quantity', 'price']
    list_display = ['id', 'product', 'product_model', 'product_description', 'prod_photo', 'prod_is_published',
                    'quantity', 'price', 'user_name', 'user_email']
    list_display_links = ['id', 'product', 'product_model', 'product_description', 'prod_photo', 'quantity',
                          'price', 'user_name', 'user_email']
    search_fields = ['user', 'product', 'quantity', 'price']
    list_filter = ['user', 'product', 'quantity', 'price']
    save_on_top = True

    @admin.display(description='Модель')
    def product_model(self, warehouse: Warehouse):
        """ Выводим модель товара """
        if warehouse.product:
            return warehouse.product.model_product
        return f"Продукт удален"

    @admin.display(description='Описание')
    def product_description(self, warehouse: Warehouse):
        """ Выводим описание товара """
        if warehouse.product:
            return warehouse.product.description
        return f"Продукт удален"

    @admin.display(description='В продаже')
    def prod_is_published(self, warehouse: Warehouse):
        """ Выводим наименование Организации """
        if warehouse.product:
            return warehouse.product.is_published
        return f"Продукт удален"

    @admin.display(description='Изображение')
    def prod_photo(self, warehouse: Warehouse):
        """ Отображение фото в админке """
        if warehouse.product:                                # TODO: картинка не отображается
            if warehouse.product.photo:
                return mark_safe(f"<img src='{warehouse.product.photo.url}' width=50>")
            return "Без фото"
        return f"Продукт удален"

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
