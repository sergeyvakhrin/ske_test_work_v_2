from django import forms

from products.models import Warehouse
from users.servises import validate_warehouse


class FormWarehouse(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'

    def clean(self):
        """ Проверяем введенные данные при создании записи в складе """
        user = self.cleaned_data.get('user')
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity')
        price = self.cleaned_data.get('price')

        validate_warehouse(user, product, quantity, price)
        Warehouse.objects.filter(quantity=0).delete()

        return self.cleaned_data
