from django import forms


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
