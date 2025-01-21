from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination


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
