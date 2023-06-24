from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from django.conf import settings
from core.celery import app as celery_app

__all__ = ('celery_app',)


@celery_app.task(bind=True)
def send_reset_password_email(email, token):
    subject = "Reset your commercify password"
    message = f"Hey, \nDid you forget your password, click the link bellow to reset your password \n http://localhost:3000/reset-password/{token}"
    sender = settings.EMAIL_HOST_USER
    reciever = [email]
    send_mail(subject, message, sender, reciever)
    return True
