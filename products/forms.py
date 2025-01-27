from django import forms

from products.models import Warehouse, Product
from users.models import User
from users.servises import validate_warehouse


class AdminFormWarehouse(forms.ModelForm):
    """ Форма для Админ панели для вывода сообщений """
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


class FormWarehouse(forms.ModelForm):
    """ Форма для Админ панели для вывода сообщений """
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

    def __init__(self, *args, **kwargs):
        """ Получаем доступ к queryset для фильтрации ForeignKey выводимых данных в форму создания
        https://medium.com/analytics-vidhya/django-how-to-pass-the-user-object-into-form-classes-ee322f02948c"""
        self.request = kwargs.pop('request')
        super(FormWarehouse, self).__init__(*args, **kwargs)
        user = self.request.user

        supplier = user.supplier
        warehouse = Warehouse.objects.filter(user=supplier)
        pk_list = [i.product_id for i in warehouse]

        if not user.is_staff or not user.is_superuser:
            self.fields['user'].queryset = User.objects.filter(email=user.email)
            self.fields['product'].queryset = Product.objects.filter(pk__in=pk_list)
        else:
            self.fields['user'].queryset = User.objects.filter(is_staff=False, is_superuser=False)
        # self.fields['user'].disabled = True


class FormWarehouseBuy(forms.ModelForm):
    """ Форма для создания записи в складе по кнопке Купить """
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

    def __init__(self, *args, **kwargs):
        """ Получаем доступ к queryset для фильтрации ForeignKey выводимых данных в форму создания
        https://medium.com/analytics-vidhya/django-how-to-pass-the-user-object-into-form-classes-ee322f02948c"""
        self.request = kwargs.pop('request')
        super(FormWarehouseBuy, self).__init__(*args, **kwargs)
        user = self.request.user

        supplier = user.supplier
        warehouse = Warehouse.objects.filter(user=supplier)
        pk_list = [i.product_id for i in warehouse]

        if not user.is_staff or not user.is_superuser:
            self.fields['user'].queryset = User.objects.filter(email=user.email)
            self.fields['product'].queryset = Product.objects.filter(pk__in=pk_list) # TODO: выводить только выбранный товар
        else:
            self.fields['user'].queryset = User.objects.filter(is_staff=False, is_superuser=False)



class ProductCreateForm(forms.ModelForm):
    """ Форма для модели Продукт """
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)

        self.fields['release_date'] = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
        'class': 'form-control'}),
        label='Укажите дату выхода на рынок',
        required=True,
        input_formats=['%Y-%m-%d', '%d-%m-%Y']
        )
