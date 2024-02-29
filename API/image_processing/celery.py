from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'API.settings')

app = Celery('API')
app.conf.enable_utc = False

app.conf.update(timezone = 'America/Denver')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat Settings here

app.conf.beat_schedule = {
    'scrape_webcams_every_2_minutes': {
        'task': 'tasks.scrape_webcams',  # path to your task
        'schedule': 120.0,  # Run every 120 seconds (2 minutes)
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_tasks(self):
    print(f'Request: {self.request!r}')