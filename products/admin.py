from django.contrib import admin
from django.db.models import Sum
from django.utils.safestring import mark_safe

from products.models import Product, Warehouse
from users.models import User
from users.servises import validate_quantity, correct_quantity_supplier


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Выводим в админ панель таблицу номенклатуры продуктов """
    list_display = ['id', 'name', 'model_product', 'description', 'prod_photo', 'is_published', 'release_date']
    list_display_links = ['id', 'name', 'model_product', 'description', 'prod_photo', 'is_published', 'release_date']
    search_fields = ['name', 'model_product', 'description', 'is_published', 'release_date']
    list_filter = ['name', 'model_product', 'description', 'is_published', 'release_date']
    save_on_top = True

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
    fields = ['user', 'product', 'quantity', 'price']
    list_display = ['id', 'product', 'product_model', 'product_description', 'prod_photo', 'quantity', 'price', 'user_name', 'user_email']
    list_display_links = ['id', 'product', 'product_model', 'product_description', 'prod_photo', 'quantity', 'price', 'user_name', 'user_email']
    search_fields = ['user', 'product', 'quantity', 'price']
    list_filter = ['user', 'product', 'quantity', 'price']
    save_on_top = True


    def save_model(self, request, obj, form, change):
        """
        Добавляем сумму задолженности перед поставщиком.
        Проверяем наличие у поставщика товара у поставщика.
        Уменьшаем количество товара у поставщика на складе.
        """
        user = form.cleaned_data.get('user')
        if user and user.client_type != 'FACTORY':
            supplier = user.supplier
            product = form.cleaned_data.get('product')
            warehouse_supplier = Warehouse.objects.filter(user=supplier, product=product)
            warehouse = warehouse_supplier.aggregate(Sum('quantity')).get('quantity__sum')

            if warehouse:
                validate_quantity(user, obj, warehouse)
                super().save_model(request, obj, form, change)
                # raise f'У поставщика только {warehouse} штук на складе.' # TODO: добавить вывод в админку
            else:
                obj.quantity = 0 # TODO: добавить валидацию поля debt на 0 и None, что бы убрать этот костыль

            correct_quantity_supplier(warehouse_supplier, obj)

        super().save_model(request, obj, form, change)
        Warehouse.objects.filter(quantity=0).delete()

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
