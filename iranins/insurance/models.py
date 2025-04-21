import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.utils import jalali

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class Insured(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('owner'), related_name='insureds')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name=_('category'), related_name='insureds')
    name = models.CharField(max_length=100, verbose_name=_('name'), null=False, blank=False)
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name=_('joined at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('insured')
        verbose_name_plural = _('insureds')

    def __str__(self):
        return self.name


class Insurance(models.Model):
    THIRD_PARTY = 1
    COMPREHENSIVE = 2
    FIRE = 3
    LIABILITY = 4

    choices = (
        (THIRD_PARTY, 'شخص ثالث'),
        (COMPREHENSIVE, 'بدنه'),
        (FIRE, 'آتش سوزی'),
        (LIABILITY, 'مسئولیت'),
    )

    insurance_number = models.CharField(max_length=50, verbose_name=_('insurance number'), null=True, blank=True)
    insurer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('insurer'), related_name='insurances')
    insured = models.ForeignKey(Insured, on_delete=models.CASCADE, verbose_name=_('insured'), related_name='insurances')
    insurance_type = models.PositiveSmallIntegerField(choices=choices, verbose_name=_('insurance type'), default=THIRD_PARTY)
    start_at = models.DateField(verbose_name=_('start at'), null=False, blank=False)
    end_at = models.DateField(verbose_name=_('end at'), null=False, blank=False)
    amount = models.PositiveBigIntegerField(verbose_name=_('amount'), null=False, blank=False)
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))

    class Meta:
        verbose_name = _('insurance')
        verbose_name_plural = _('insurances')

    def __str__(self):
        return f'{self.insured}'

    def days_remaining(self):
        remaining = (self.end_at - datetime.date.today()).days
        return remaining

    def abs_days_remaining(self):
        return abs(self.days_remaining())

    def days_remaining_percentage(self):
        remain = self.days_remaining()
        percent = (remain / 365) * 100

        if int(percent) > 100:
            return 100
        elif int(percent) < 0:
            return 0

        return int(percent)

    @classmethod
    def open_insurance(cls, insurer, insured, data):
        type = data.get('insurance_type')
        insurance_number = data.get('insurance_number')
        start_date = cls.convert_date(data.get('start_at'))
        end_date = cls.convert_date(data.get('end_at'))
        amount = int(data.get('amount'))

        if type == 'third-party':
            insurance_type = cls.THIRD_PARTY
        elif type == 'comprehensive':
            insurance_type = cls.COMPREHENSIVE
        elif type == 'fire':
            insurance_type = cls.FIRE
        elif type == 'liability':
            insurance_type = cls.LIABILITY

        instance = cls.objects.create(insurance_number=insurance_number, insurer=insurer, insured=insured,
                           amount=amount, insurance_type=insurance_type, start_at=start_date, end_at=end_date)

        return instance

    @classmethod
    def convert_date(cls, data):
        date = data.split('/')
        return jalali.Persian(int(date[0]), int(date[1]), int(date[2])).gregorian_datetime()

    def paid_installments_count(self):
        return self.installments.filter(is_complete=True).count()

    def get_installments(self):
        return self.installments.all().order_by('start_at')

class Attribute(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('attribute')
        verbose_name_plural = _('attributes')

    def __str__(self):
        return self.name


class InsuredAttributeValue(models.Model):
    insured = models.ForeignKey(Insured, on_delete=models.CASCADE, verbose_name=_('insured'), related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name=_('attribute'), related_name='insureds')
    value = models.CharField(max_length=100, verbose_name=_('value'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('insured attribute value')
        verbose_name_plural = _('insured attribute values')

    def __str__(self):
        return f'{self.attribute}: {self.value}'

