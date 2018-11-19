from datetime import timedelta
from time import timezone

from celery import shared_task

from dream import settings
from django.template.loader import render_to_string
from dream_users import models as user_models

from core.tasks import send_email


def generate_confirm_link(email):
    user = user_models.User.objects.get(email=email)
    token = user_models.ConfirmEmailToken.objects.create(user=user)
    return '{host}/confirm/{token}/'.format(host=settings.SERVER_URL, token=token.token)


def generate_forgot_link(email):
    user = user_models.User.objects.get(email=email)
    reset_token = user_models.ResetToken.objects.create(user=user)
    return '{host}/forgot-link/{token}'.format(host=settings.SERVER_URL, token=reset_token.reset_token)


@shared_task
def send_register_confirm_email(to_email):
    confirm_link = generate_confirm_link(to_email)
    subject = '[Sixcent English App] Register Confirmation'
    context = {'confirm_link': confirm_link}
    body_html = render_to_string('emails/register_confirm.html', context)
    send_email.delay(
        subject=subject,
        body_html=body_html,
        from_email=settings.EMAIL_NO_REPLY,
        recipient_list=[to_email]
    )


@shared_task
def send_register_confirm_email(to_email):
    confirm_link = generate_confirm_link(to_email)
    subject = '[Sixcent English App] Register Confirmation'
    context = {'confirm_link': confirm_link}
    body_html = render_to_string('emails/register_confirm.html', context)
    send_email.delay(
        subject=subject,
        body_html=body_html,
        from_email=settings.EMAIL_NO_REPLY,
        recipient_list=[to_email]
    )


@shared_task
def send_forgot_password_email(to_email):
    forgot_link = generate_forgot_link(to_email)
    subject = '[Sixcent English App] Forgot password'
    context = {'forgot_link': forgot_link}
    body_html = render_to_string('emails/forgot_password.html', context)
    send_email.delay(
        subject=subject,
        body_html=body_html,
        from_email=settings.EMAIL_NO_REPLY,
        recipient_list=[to_email]
    )
