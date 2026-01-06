from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 1️Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

# 2️Create the Celery app
app = Celery('alx_travel_app')

# 3️Load settings from Django's settings.py (CELERY_BROKER_URL, etc.)
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4️Automatically discover tasks.py in installed apps
app.autodiscover_tasks()

# 5️Optional: simple debug log
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
