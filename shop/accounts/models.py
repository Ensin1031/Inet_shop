from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class ShopUser(AbstractUser):
    """"""
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Активирован?')
    phone_number = PhoneNumberField(unique=True, blank=True, null=True,
                                    verbose_name='Номер телефона')
    address = models.TextField(max_length=300, blank=True, null=True,
                               verbose_name='Полный адрес')

    class Meta(AbstractUser.Meta):
        pass


