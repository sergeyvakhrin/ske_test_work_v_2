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


class CustomPagination(PageNumberPagination):
    """Контроль количества результатов на странице"""
    page_size = 5
    max_page_size = 100
    page_size_query_param = "page_size"


def validate_quantity(user, obj, warehouse):
    """ Контроль количества закупки """
    if warehouse < obj.quantity:
        user.debt += warehouse * obj.price
        obj.quantity = warehouse
        user.save()
    if warehouse >= obj.quantity:
        user.debt += obj.quantity * obj.price
        user.save()
    return user

def correct_quantity_supplier(warehouse_supplier, obj):
    """ Корректирование остатков поставщика """
    for warehouse_quantity in warehouse_supplier:
        if warehouse_quantity.quantity >= obj.quantity:
            warehouse_quantity.quantity -= obj.quantity
            warehouse_quantity.save()
            break
        elif warehouse_quantity.quantity < obj.quantity:
            warehouse_quantity.quantity = 0
            obj.quantity -= warehouse_quantity.quantity
            warehouse_quantity.save()
            continue
