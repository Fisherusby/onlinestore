from smtplib import SMTPAuthenticationError

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def notify_order(order):
    subject = f'Thank you for your order №{str(order.pk).rjust(10,"0")}'
    # message = f'Thank you for your order №{str(order.pk).rjust(10,"0")}'

    html_message = render_to_string('emails/order_create.html', {'order': order})
    plain_message = strip_tags(html_message)

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [order.user.email, email_from]

    try:
        send_mail(subject, plain_message, email_from, recipient_list)
    except SMTPAuthenticationError:
        print(SMTPAuthenticationError.smtp_error)
        return False

    return True
