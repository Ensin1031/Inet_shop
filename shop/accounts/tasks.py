from .models import ShopUser
from .utilities import send_activation_notification
from shop.celery import app


@app.task
def send_activation_mail(user_id):

    """The function of determining the user object of
    the model ShopUser by id and sending mails for activation"""

    user = ShopUser.objects.get(pk=user_id)
    send_activation_notification(user)
