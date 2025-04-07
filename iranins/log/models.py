from django.conf import settings
from django.db import models
import jdatetime


class Log(models.Model):
    CREATE = 1
    EDIT = 2
    DELETE = 3

    choices = (
        (CREATE, 'ایجاد'),
        (EDIT, 'ویرایش'),
        (DELETE, 'حذف'),
    )

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='from_logs')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to_logs')
    operation = models.PositiveSmallIntegerField(choices=choices, default=CREATE)
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    @classmethod
    def create_log(cls, from_user, to_user, operation, data):
        instance = cls.objects.create(from_user=from_user, to_user=to_user, operation=operation)
        instance.description = 'کاربر {} داده {} را برای کاربر {} {} کرد.'.format(from_user,
                                                                                              data, to_user,
                                                                                              instance.get_operation_display())
        instance.save()
