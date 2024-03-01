from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'API.settings')

app = Celery('API')
app.conf.enable_utc = False

app.conf.update(timezone = 'America/Denver')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat Settings here

# app.conf.beat_schedule = {
#     'scrape_webcams_every_2_minutes': {
#         'task': 'image_processing.tasks.scrape_webcams',  # path to your task
#         'schedule': 120.0,  # Run every 180 seconds (3 minutes)
#     },
# }

app.conf.beat_schedule = {
    # Monday to Thursday: 6 a.m. to Midnight
    'every-two-minutes-monday-to-thursday': {
        'task': 'image_processing.tasks.scrape_webcams',
        'schedule': crontab(minute='*/2', hour='6-23', day_of_week='mon,tue,wed,thu'),
    },
    # Friday: 6 a.m. to 11 p.m.
    'every-two-minutes-friday': {
        'task': 'image_processing.tasks.scrape_webcams',
        'schedule': crontab(minute='*/2', hour='6-22', day_of_week='fri'),
    },
    # Saturday: 8 a.m. to 11 p.m.
    'every-two-minutes-saturday': {
        'task': 'image_processing.tasks.scrape_webcams',
        'schedule': crontab(minute='*/2', hour='8-22', day_of_week='sat'),
    },
    # Sunday: 8 a.m. to Midnight
    'every-two-minutes-sunday': {
        'task': 'image_processing.tasks.scrape_webcams',
        'schedule': crontab(minute='*/2', hour='8-23', day_of_week='sun'),
    },
}


app.autodiscover_tasks()

@app.task(bind=True)
def debug_tasks(self):
    print(f'Request: {self.request!r}')
