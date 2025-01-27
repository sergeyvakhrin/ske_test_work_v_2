from django.db.models import Sum
from django import forms
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination

from products.models import Warehouse


class IsOwner(permissions.BasePermission):
    """ Проверяем права на просмотр, редактирование и удаление"""
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False


class IsModer(permissions.BasePermission):
    def has_permission(self, request, view):
        """ Проверяем на принадлежность к группе. """
        return request.user.groups.filter(name='Moderators').exists()


class UsersCustomPagination(PageNumberPagination):
    """Контроль количества результатов на странице"""
    page_size = 5
    max_page_size = 100
    page_size_query_param = "page_size"


def validate_warehouse(user, product, quantity, price):
    """ Проверка введенных данный при создании записи на складе. """
    if not product.is_published:
        raise forms.ValidationError('Продукт запрещен к реализации!!!')
    else:
        if user and user.client_type != 'FACTORY':
            supplier = user.supplier
            warehouse_supplier = Warehouse.objects.filter(user=supplier, product=product)
            warehouse = warehouse_supplier.aggregate(Sum('quantity')).get('quantity__sum')
            if warehouse:
                if quantity == 0 or quantity is None:
                    raise forms.ValidationError('Укажите количество.')
                if warehouse < quantity:
                    raise forms.ValidationError(f'У поставщика {warehouse} штук на складе.')
                if price == 0 or price is None:
                    raise forms.ValidationError('Укажите цену.')
                validate_quantity(user, quantity, price, warehouse)
                correct_quantity_supplier(warehouse_supplier, quantity)
            else:
                raise forms.ValidationError(f'У поставщика нет этого товара на складе.')
        else:
            if quantity == 0 or quantity is None:
                raise forms.ValidationError('Укажите количество.')
            if price == 0 or price is None:
                raise forms.ValidationError('Укажите цену.')


def validate_quantity(user, quantity, price, warehouse):
    """ Контроль количества закупки """
    if warehouse < quantity:
        user.debt += warehouse * price
        quantity = warehouse
        user.save()
    if warehouse >= quantity:
        user.debt += quantity * price
        user.save()
    return user

def correct_quantity_supplier(warehouse_supplier, quantity) -> None:
    """ Корректирование остатков поставщика """
    for warehouse_quantity in warehouse_supplier:
        if warehouse_quantity.quantity >= quantity:
            warehouse_quantity.quantity -= quantity
            warehouse_quantity.save()
            break
        elif warehouse_quantity.quantity < quantity:
            warehouse_quantity.quantity = 0
            quantity -= warehouse_quantity.quantity
            warehouse_quantity.save()
            continue
