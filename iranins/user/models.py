from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from user.managers import CustomUserManager


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, verbose_name=_('phone'))
    national_id = models.CharField(max_length=10, unique=True, verbose_name=_('national id'), null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ('username', )

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.phone

