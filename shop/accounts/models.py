from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    """"""
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
        pass
