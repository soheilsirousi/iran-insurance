from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from django_celery_beat.models import PeriodicTask, CrontabSchedule
        from django.db.utils import OperationalError
        schedule, _ = CrontabSchedule.objects.get_or_create(minute='55', hour='23')

        PeriodicTask.objects.get_or_create(
            crontab=schedule,
            name='remind_installments',
            task='user.tasks.remind_installments',
            defaults={'enabled': True},
        )