from rest_framework import serializers

from products.models import Product, Warehouse


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Product """
    class Meta:
        model = Product
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Product """
    class Meta:
        model = Warehouse
        fields = '__all__'
