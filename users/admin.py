from django.contrib import admin

from products.models import Warehouse
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Выводим в админ панель таблицу пользователей """
    list_display = ['id','name', 'email', 'client_type', 'country', 'city', 'street', 'house_number',
                    'created_at', 'supplier_name', 'product_list', 'debt']
    list_display_links = list_display
    exclude = ['password', 'last_name', 'first_name', 'last_login', 'date_joined', 'debt']
    search_fields = ('city', 'name', 'client_type')
    list_filter = ('city', 'name', 'client_type')
    actions = ['set_debt_zero']
    save_on_top = True

    @admin.display(description='Поставщик')
    def supplier_name(self, user: User):
        """ Выводим название поставщика """
        return user.supplier

    @admin.display(description='Список товаров')
    def product_list(self, user: User):
        """ Выводим список продуктов конкретного завода """
        warehouses = Warehouse.objects.filter(user=user)
        if warehouses:
            products_name = []
            for warehous in warehouses:
                products_name.append(warehous.product.name)
            if len(products_name) > 0:
                return products_name
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
