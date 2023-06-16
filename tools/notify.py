from smtplib import SMTPAuthenticationError

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_notyfy(subject, html_message, address_to):
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [address_to, email_from]

    try:
        send_mail(subject, plain_message, email_from, recipient_list)
    except SMTPAuthenticationError:
        return False


def notify_order(order):
    subject = f'Новый заказ N{str(order.pk).rjust(10,"0")}'
    html_message = render_to_string("emails/order_create.html", {"order": order})
    send_to = order.user.email

    return send_notyfy(subject, html_message, send_to)


def notify_payment(receipt):
    subject = f'Изменение статуса заказа N{str(receipt.order.pk).rjust(10,"0")}'
    html_message = render_to_string("emails/order_payment.html", {"receipt": receipt})
    send_to = receipt.order.user.email

    return send_notyfy(subject, html_message, send_to)
