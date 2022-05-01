from shop.celery import app
from .models import ShopUser
from .utilities import send_activation_notification


@app.task
def send_activation_mail(user_id):
    user = ShopUser.objects.get(pk=user_id)
    send_activation_notification(user)
