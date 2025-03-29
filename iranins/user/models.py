from django.contrib.auth import login
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

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
    image = models.ImageField(upload_to='user/', verbose_name=_('image'), null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ('username', )

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.phone

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
    def create_user(cls, data, file):
        phone = data.get("mobile")
        national_id = data.get("national_id")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        role = data.get("role")
        profile_image = file.get('profile_image')

        if role == 'owner':
            role = 1
        elif role == 'support':
            role = 2
        elif role == 'customer':
            role = 3

        password = cls.objects.make_random_password()
        user = cls.objects.create_user(phone=phone, national_id=national_id,
                                              first_name=first_name, last_name=last_name, role=role, password=password)

        if profile_image:
            file_name = f'user/{user.username}_{profile_image.name}'
            path = default_storage.save(file_name, ContentFile(profile_image.read()))

            user.image = path

        user.save()


    @classmethod
    def edit_user(cls, user, data, file):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        national_id = data.get('national_id')
        role = data.get('role')
        profile_image = file.get('profile_image')

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

        if profile_image:
            file_name = f'user/{user.username}_{profile_image.name}'
            path = default_storage.save(file_name, ContentFile(profile_image.read()))

            user.image = path

        user.save()