from smtplib import SMTPAuthenticationError

from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "reset_password_url": "{}?token={}".format(
            instance.request.build_absolute_uri(reverse("password_reset:reset-password-confirm")),
            reset_password_token.key,
        ),
    }

    email_html_message = render_to_string("email/user_reset_password.html", context)

    subject = "Password Reset for {title}".format(title="Some website title")

    plain_message = strip_tags(email_html_message)

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [reset_password_token.user.email]

    try:
        send_mail(subject, plain_message, email_from, recipient_list)
    except SMTPAuthenticationError:
        print(SMTPAuthenticationError.smtp_error)
        return False
