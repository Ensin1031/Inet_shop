from django.db import models
from django.conf import settings
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import ShopUser
from shopping.models import GoodsDB


class OrderDB(models.Model):
    """Checkout Model"""
    ACCEPTED = 'NR'
    SENT = 'SE'
    STATUS_CHOICES = (
        (ACCEPTED, 'На рассмотрении'),
        (SENT, 'Отправлен'),
    )

    POST_RUSSIA = 'PR'
    COURIER_DELIVERY = 'CD'
    EXPRESS_COURIER_DELIVERY = 'ED'
    DELIVERY_CHOICES = (
        (POST_RUSSIA, 'Получите Ваш заказ в отделении Почты России'),
        (COURIER_DELIVERY, 'Заберите Ваш заказ в офисе курьерской службы'),
        (EXPRESS_COURIER_DELIVERY, 'Ваш товар доставят Вам домой курьером'),
    )

    for_user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, null=True,
                                 related_name='order_user_name', verbose_name='Покупатель')
    postal_code = models.PositiveBigIntegerField(verbose_name='Почтовый индекс')
    country = models.CharField(default='Российская Федерация', max_length=100, verbose_name='Страна')
    region = models.CharField(max_length=100, default='Хабаровский край', verbose_name='Регион')
    city = models.CharField(max_length=100, default='Хабаровск', verbose_name='Населенный пункт')
    address = models.CharField(max_length=150, verbose_name='Адрес')
    phone_number = PhoneNumberField(verbose_name='Номер телефона')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=ACCEPTED, verbose_name='Статус заказа')
    date_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    date_up = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения записи')
    delivery_type = models.CharField(max_length=2, choices=DELIVERY_CHOICES, default=POST_RUSSIA,
                                     verbose_name='Выберите тип доставки')

    def __str__(self):
        return f'Запись покупки № {self.id}'

    def get_total_price(self):
        """Получить ИТОГО за товары, купленные в этом заказе."""
        return sum(item.get_cost() for item in self.items.all())

    def get_absolute_url(self):
        return reverse('orders:order_created', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-date_up',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы(ов)'


class OrderItemDB(models.Model):
    """Модель данных о покупаемых товарах"""
    order = models.ForeignKey(OrderDB, on_delete=models.PROTECT, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(GoodsDB, on_delete=models.PROTECT, related_name='order_items', verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена при покупке')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        """Получить ИТОГО за данный товар"""
        return self.price * self.quantity

    class Meta:
        ordering = ('-order',)
        verbose_name = 'Товар(а)'
        verbose_name_plural = 'Товары(ов)'


