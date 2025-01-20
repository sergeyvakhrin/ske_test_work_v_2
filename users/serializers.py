from rest_framework import serializers
from rest_framework.exceptions import APIException

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели User """
    buyers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "email",
            "name",
            "country",
            "city",
            "street",
            "house_number",
            "client_type",
            "created_at",
            "debt",
            "supplier",
            "groups",
            "user_permissions",
            "buyers"
        ]

    def validate_supplier(self, value):
        """
        Генерирует ошибку при попытке назначить поставщика Заводу
        Генерирует ошибку при создании пользователя без поставщика
        """
        if self.initial_data.get('client_type') == 'FACTORY' and value:
            raise APIException("У Завода не может быть поставщика готовой продукции.")
        if self.initial_data.get('client_type') != 'FACTORY' and value is None:
            raise APIException("Необходимо указать поставщика.")
        return value

    def get_buyers(self, instance):
        """ Метод получения списка Покупателей """
        buyers = instance.user_supplier.all()
        if buyers:
            return UserSerializer(buyers, many=True).data
        return 0