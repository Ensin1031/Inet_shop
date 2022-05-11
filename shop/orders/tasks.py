from .models import OrderDB
from .utilities import send_admin_neworder, send_order_notification
from accounts.models import ShopUser
from shop.celery import app


@app.task
def send_admin_mail(order_id, user_id):
    """
    The function of determining the order object of
    the model OrderDB, the user object of the model ShopUser
    by id and sending mails to admin about new orders
    """

    order = OrderDB.objects.get(pk=order_id)
    user = ShopUser.objects.get(pk=user_id)
    send_admin_neworder(order, user)


@app.task
def send_order_mail(order_id, user_id):
    """
    The function of determining the order object of
    the model OrderDB, the user object of the model ShopUser
    by id and sending mails to users about orders dispatchment
    """

    order = OrderDB.objects.get(pk=order_id)
    user = ShopUser.objects.get(pk=user_id)
    send_order_notification(order, user)
