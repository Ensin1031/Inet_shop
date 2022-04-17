# from django.contrib.auth.models import User
# from django.db import models
# from django.urls import reverse
# from uuslug import uuslug
# from autoslug import AutoSlugField
#
# from shopping.models import GoodsDB
#
#
# def instance_slug(instance):
#     return instance.title
#
#
# def slugify_value(value):
#     return value.replace(' ', '-')
#
#
# class BasketDB(models.Model):
#     product = models.ManyToManyField(GoodsDB, verbose_name='Товары', related_name="relCart")
#     total = models.FloatField(verbose_name='Сумма', default=0)
#     date_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания карточки')
#     session_id = models.UUIDField(max_length=100, verbose_name='ID сессии')
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='buyer_user',
#                                 verbose_name='Покупатель')
#
#     def __str__(self):
#         return str(self.session_id)
#
#     class Meta:
#         verbose_name = 'Карточка покупки'
#         verbose_name_plural = 'Карточки покупок'
#         ordering = ('-date_at',)
#
#
# class CartDB(models.Model):
#     ...
#
