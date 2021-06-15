from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rest_api.settings")

app = Celery("rest_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.timezone = "Europe/Moscow"

app.autodiscover_tasks()
