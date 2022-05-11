from django import forms

from .models import OrderDB

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """
    Form to add the to the basket
    """

    quantity = forms.TypedChoiceField(
            label='Количество',
            choices=PRODUCT_QUANTITY_CHOICES,
            coerce=int,  # идет автоматическое преобразование в целое число
    )
    update = forms.BooleanField(
            required=False,
            initial=False,
            widget=forms.HiddenInput
    )


class OrderCreateForm(forms.ModelForm):
    """
    Form for creating an order record in the model OrderDB
    """

    class Meta:
        model = OrderDB
        fields = ('postal_code', 'country', 'region', 'city', 'address',
                  'phone_number', 'delivery_type',)
