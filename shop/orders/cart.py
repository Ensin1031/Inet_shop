from django.conf import settings

from decimal import Decimal

from shopping.get_func import get_promo
from shopping.models import GoodsDB


class Cart(object):
    """
    Order basket session class
    """

    def __init__(self, request):
        self.session = request.session  # получаем данные из сессии
        cart = self.session.get(
            settings.CART_SESSION_ID)  # пытаемся получить данные в корзину
        if not cart:
            # сохраняем ПУСТУЮ корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        if self.cart:
            self.products = GoodsDB.objects.filter(
                id__in=self.cart.keys()).prefetch_related('images_for_goods')

    def __iter__(self):
        # получаем товары и добавляем их в корзину
        if self.cart:
            cart = self.cart.copy()
            for product in self.products:
                cart[str(product.id)]['product'] = product

            for item in cart.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, good, quantity=1, update_quantity=False):
        """
        The function to add a good to the basket or update the quantity
        of good in the basket
        """
        product_id = str(good.id)
        if product_id not in self.cart:  # делаем преобразование в JSON
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(round(good.price * get_promo(good), 2)),
            }
        if update_quantity:  # преобразуем количество единиц товара в корзине
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        """
        The function to remove the good from the basket
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """
        The function to return the total basket cost
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        """
        The fuction to clear the session basket
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    # def testing_print(self, a='work basket'):
    #     print(f'test {a}')
    #     return f'test_print {a}'
