from django.contrib import admin

from products.models import Warehouse
from users.management.commands.csu import Command
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Выводим в админ панель таблицу пользователей """
    list_display = ['id','name', 'email', 'client_type', 'country', 'city', 'street', 'house_number',
                    'created_at', 'supplier_name', 'product_list', 'debt']
    list_display_links = list_display
    exclude = ['last_name', 'first_name', 'last_login', 'date_joined', 'debt']
    search_fields = ('city', 'name', 'client_type')
    list_filter = ('city', 'name', 'client_type')
    actions = ['set_debt_zero']
    save_on_top = True

    def save_model(self, request, obj, form, change):
        """ Хэшируем пароль """
        if "password" in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        """ Перепривязываем покупателей к следующему по иерархии поставщику, если удален текущий """
        for user in queryset:       # TODO: добавить запрет на удаление, если есть товар на складе
            if user.supplier:
                User.objects.filter(supplier=user).update(supplier=user.supplier)
        queryset.delete()

    @admin.display(description='Поставщик')
    def supplier_name(self, user: User):
        """ Выводим название поставщика """
        return user.supplier

    @admin.display(description='Список товаров')
    def product_list(self, user: User):
        """ Выводим список продуктов пользователя """
        warehouses = Warehouse.objects.filter(user=user)
        if warehouses:
            products_name = []
            for warehous in warehouses:
                products_name.append(warehous.product.name)
            products_name = set(products_name)
            if len(products_name) > 0:
                return list(products_name)
        return 'Нет продуктов'

    def get_readonly_fields(self, request, obj=None):
        """ Делаем поля только для чтения, если просмотр """ # TODO: упростить каскад условий
        if obj:
            if obj.supplier_id is None:
                if obj.client_type == 'FACTORY':
                    return self.readonly_fields + ('client_type', 'supplier', 'debt',)
                return self.readonly_fields + ('client_type', 'debt',)
            return self.readonly_fields + ('client_type', 'supplier', 'debt',)
        return self.readonly_fields

    # def get_exclude(self, request, obj=None):
    #     """ Исключаем поля у Завода """  # TODO: Не работает...
    #     if obj.client_type == 'FACTORY':
    #         self.exclude += ('debt', 'supplier', )
    #         return self.exclude
    #     return self.exclude

    @admin.action(description='Обнулить задолженность перед поставщиком')
    def set_debt_zero(self, request, queryset):
        """ Логика дополнительного действия """
        count = queryset.update(debt=0)
        self.message_user(request, f'Изменено {count} записей')
