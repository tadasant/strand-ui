import os
from celery import Celery

# Runs separately from manage.py runserver
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

app = Celery('app')

# Loads all config variables that begin with CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all register Django app configs
app.autodiscover_tasks()
