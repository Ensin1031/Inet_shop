from accounts.models import ShopUser
from shop.celery import app
from .models import OrderDB
from .utilities import send_admin_neworder, send_order_notification


@app.task
def send_admin_mail(order_id):
    order = OrderDB.objects.get(pk=order_id)
    send_admin_neworder(order)


@app.task
def send_order_sent(user_id):
    user = ShopUser.objects.get(pk=user_id)
    send_order_notification(user)
