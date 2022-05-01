from django import forms

from accounts.models import ShopUser
from .models import OrderDB


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """Класс формы добавления товара в корзину."""
    quantity = forms.TypedChoiceField(
        label='Количество',
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,     # идет автоматическое преобразование в целое число.
        # widget=forms.Select(attrs={'class': "horizontal-quantity"})
    )
    update = forms.BooleanField(required=False,     # поле обновить
                                initial=False,
                                widget=forms.HiddenInput)


class ToBuyForm(forms.Form):
    '''добавляем флажок Покупать/Не покупать'''
    select_to_buy = forms.BooleanField(initial=True)


# class OrderCreateForm(forms.ModelForm):
#     """Form for creating an order record in the model OrderDB"""
#     class Meta:
#         model = OrderDB
#         fields = ('first_name', 'last_name', 'postal_code', 'country',
#                   'region', 'city', 'address', 'phone_number', 'delivery_type',)


class OrderCreateForm(forms.ModelForm):
    """Form for creating an order record in the model OrderDB"""
    class Meta:
        model = OrderDB
        fields = ('postal_code', 'country',
                  'region', 'city', 'address', 'phone_number', 'delivery_type',)

