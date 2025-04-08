import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iranins.settings")

celery_app = Celery("iranins")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()


celery_app.conf.beat_schedule = {
    'remind_installments': {
        'task': 'user.tasks.remind_installments',
        'schedule': crontab(hour=10, minute=37),
    },
}