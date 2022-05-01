from django.template.loader import render_to_string
from django.core.mail import mail_admins

from shop.settings import ALLOWED_HOSTS


def send_admin_neworder(order):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'order': order, 'host': host}
    subject = render_to_string('email/admin_order_subject.txt', context)
    body_text = render_to_string('email/admin_order_body.txt', context)
    mail_admins(subject, body_text)


def send_order_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'user': user, 'host': host}
    subject = render_to_string('email/sent_order_subject.txt', context)
    body_text = render_to_string('email/sent_order_body.txt', context)
    user.email_user(subject, body_text)
