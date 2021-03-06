from django.core.signing import Signer
from django.template.loader import render_to_string

from shop.settings import ALLOWED_HOSTS

signer = Signer()


def send_activation_notification(user):
    """
    The function of creation and sending of activation mails to the user
    """

    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'

    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)
