from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Product """
    class Meta:
        model = Product
        fields = '__all__'
