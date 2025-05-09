import datetime
from django.contrib.auth import login
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _

from transaction.models import Balance
from user.managers import CustomUserManager
from user.utils.otp import verify_otp


class CustomUser(AbstractUser):
    OWNER = 1
    SUPPORTER = 2
    CLIENT = 3

    choices = (
        (OWNER, _('مدیر')),
        (SUPPORTER, _('پشتیبان')),
        (CLIENT, _('مشتری')),
    )

    phone = models.CharField(max_length=11, unique=True, verbose_name=_('phone'))
    national_id = models.CharField(max_length=10, unique=True, verbose_name=_('national id'), null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=choices, verbose_name=_('role'), default=CLIENT)
    on_block_list = models.BooleanField(default=False, verbose_name=_('on block list'))
    image = models.ImageField(upload_to='user/', verbose_name=_('image'), null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ('username', )

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.phone

    def get_balance(self):
        positive_amounts = Coalesce(Sum('amount', filter=Q(balance_type=1)), 0)
        negative_amounts = Coalesce(Sum('amount', filter=Q(balance_type=2)), 0)

        instance = Balance.objects.filter(user=self).aggregate(
            balance=positive_amounts - negative_amounts
        )

        return instance['balance']

    @classmethod
    def login_user(cls, request, phone, otp):
        if verify_otp(phone, otp):
            user = cls.objects.filter(phone=phone)
            if user.exists():
                user = user.first()
                if user.role != 3:
                    login(request, user)
                else:
                    return False, "دسترسی به این صفحه برای مشتریان محدود است."
            else:
                return False, "کاربر در سیستم وجود ندارد."

            return True, "ورود موفق"

        return False, "رمز یکبار مصرف نادرست است."

    @classmethod
    def create_user(cls, data):
        phone = data.get("mobile")
        national_id = data.get("national_id")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        role = data.get("role")
        is_block = data.get("is_block")
        block = False

        if is_block == 'on':
            block = True

        if role == 'owner':
            role = 1
        elif role == 'support':
            role = 2
        elif role == 'customer':
            role = 3

        password = cls.objects.make_random_password()
        user = cls.objects.create_user(phone=phone, national_id=national_id, on_block_list=block,
                                              first_name=first_name, last_name=last_name, role=role, password=password)

        user.save()

        return user


    @classmethod
    def edit_user(cls, user, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        national_id = data.get('national_id')
        role = data.get('role')
        is_block = data.get('is_block')

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if national_id:
            user.national_id = national_id

        if role == 'owner':
            user.role = user.OWNER
        elif role == 'support':
            user.role = user.SUPPORTER
        elif role == 'customer':
            user.role = user.CLIENT

        if is_block == 'on':
            user.on_block_list = True
        else:
            user.on_block_list = False

        user.save()

    @classmethod
    def get_today(cls):
        return datetime.date.today()

    @classmethod
    def get_year_later(cls):
        today = cls.get_today()
        return datetime.date(year=today.year+1, month=today.month, day=today.day)
