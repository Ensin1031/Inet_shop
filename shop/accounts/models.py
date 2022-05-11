from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopUser(AbstractUser):
    """
    Model ShopUser to save new users to database
    """

    middle_name = models.CharField(
            max_length=150,
            blank=True,
            null=True,
            verbose_name='Отчество'
    )
    is_activated = models.BooleanField(
            default=True,
            db_index=True,
            verbose_name='Активирован?'
    )

    def get_full_name(self):
        if self.middle_name:
            full_name = "%s %s %s" % (
                self.last_name, self.first_name, self.middle_name
            )
        else:
            full_name = "%s %s " % (
                self.last_name, self.first_name
            )
        return full_name.strip()

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь(я)'
        verbose_name_plural = 'Пользователи(ей)'
        ordering = ('-date_joined',)
