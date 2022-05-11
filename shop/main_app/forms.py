from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

from .models import PromotionDB


class PromotionForm(forms.ModelForm):
    """
    Form for validating model fields
    """

    class Meta:
        model = PromotionDB
        fields = ('promo_title', 'is_active', 'discount',
                  'category', 'brand', 'photo',)

    def clean(self):
        super().clean()
        errors = {}
        category = self.cleaned_data.get('category')
        brand = self.cleaned_data.get('brand')

        if not category and not brand:
            errors[NON_FIELD_ERRORS] = ValidationError(
                    'В акции должна быть указана хотя бы одна '
                    'категория и/или один производитель'
            )
        if errors:
            raise ValidationError(errors)
