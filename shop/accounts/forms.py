from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import ShopUser
from .apps import user_registered


class RegisterUserForm(forms.ModelForm):
    """"""
    email = forms.EmailField(
            required=True,
            label='Электронная почта',
            help_text='Обязательное поле'
    )
    password1 = forms.CharField(
            label='Ваш пароль',
            widget=forms.PasswordInput,
            help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
            label='Введите пароль еще раз',
            widget=forms.PasswordInput,
            help_text='Введите тот же самый пароль еще раз для проверки'
    )
    middle_name = forms.CharField(
            required=False,
            label='Отчество',
            help_text='При наличии'
    )

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password_validation.validate_password(password1)
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                    'Введенные пароли не совпадают',
                    code='password_mismatch'
            )}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'middle_name', 'last_name')


class ChangeUserInfoForm(forms.ModelForm):
    """"""
    email = forms.EmailField(required=True, label='Электронная почта')

    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'phone_number',
                  'first_name', 'middle_name', 'last_name')


class ChangeUserAddressForm(forms.ModelForm):
    """"""

    class Meta:
        model = ShopUser
        fields = ('postcode', 'country', 'region', 'city', 'address')
