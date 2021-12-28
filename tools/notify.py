from smtplib import SMTPAuthenticationError

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def notify_order(order):
    subject = f'Thank you for your order №{str(order.pk).rjust(10,"0")}'
    message = f'Thank you for your order №{str(order.pk).rjust(10,"0")}'

    html_message = render_to_string('emails/invitation.html', {'order': order})

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [order.user.email, email_from]

    try:
        send_mail(subject, message, email_from, recipient_list)
    except SMTPAuthenticationError:
        print(SMTPAuthenticationError.smtp_error)
        return False

    return True
