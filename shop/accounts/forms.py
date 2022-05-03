from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import ShopUser
from .tasks import send_activation_mail


class RegisterUserForm(forms.ModelForm):

    """User registration form class"""

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
    first_name = forms.CharField(
            required=True,
            label='Имя',
            help_text='Обязательное поле'
    )
    middle_name = forms.CharField(
            required=False,
            label='Отчество',
            help_text='При наличии'
    )
    last_name = forms.CharField(
            required=True,
            label='Фамилия',
            help_text='Обязательное поле'
    )

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password_validation.validate_password(password1)
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            errors = {
                'password2': ValidationError('Введенные пароли не совпадают',
                                             code='password_mismatch')
            }
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        send_activation_mail.delay(user.id)
        return user

    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'middle_name', 'last_name')


class ChangeUserInfoForm(forms.ModelForm):

    """Form class for updating user personal data"""

    email = forms.EmailField(
            required=True,
            label='Электронная почта'
    )
    first_name = forms.CharField(
            required=True,
            label='Имя',
            help_text='Обязательное поле'
    )
    last_name = forms.CharField(
            required=True,
            label='Фамилия',
            help_text='Обязательное поле'
    )

    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'first_name',
                  'middle_name', 'last_name')

