from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class ShopUser(AbstractUser):
    """"""
    middle_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Отчество')
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Активирован?')
    phone_number = PhoneNumberField(unique=True, blank=True, null=True,
                                    verbose_name='Номер телефона')
    postcode = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Почтовый индекс')
    country = models.CharField(default='Российская Федерация', max_length=100, blank=True, null=True, verbose_name='Страна')
    region = models.CharField(max_length=100, blank=True, null=True, verbose_name='Регион')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Населенный пункт')
    address = models.CharField(max_length=150, blank=True, null=True, verbose_name='Адрес')

    def get_full_name(self):
        full_name = "%s %s %s" % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip()

    class Meta(AbstractUser.Meta):
        pass


