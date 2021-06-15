
from __future__ import absolute_import, unicode_literals

from django.conf import settings
import django.core.mail as dcm

from rest_api.celery import app


@app.task
def send_email(subject, html_message, recipient_list):
    dcm.send_mail(
        subject=subject,
        message=None,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
    )
