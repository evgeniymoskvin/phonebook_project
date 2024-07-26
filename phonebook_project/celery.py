import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phonebook_project.settings')

app = Celery('phonebook_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery beat tasks

app.conf.beat_schedule = {
}

# C:\projects\monitoring_tasks\venv\Scripts\python.exe C:\projects\monitoring_tasks\venv\Scripts\celery.exe  -A phonebook_project worker -l info --pool=solo
