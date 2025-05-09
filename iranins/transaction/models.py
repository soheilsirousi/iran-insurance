import datetime
import uuid
from django.conf import settings
from django.db import models
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from insurance.models import Insurance
from transaction.utils.round import round_to_nearest


class Installment(models.Model):
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name='installments', verbose_name=_('installment'))
    amount = models.PositiveBigIntegerField(verbose_name=_('amount'), null=False, blank=False)
    start_at = models.DateField(verbose_name=_('start at'), null=False, blank=False)
    end_at = models.DateField(verbose_name=_('end at'), null=False, blank=False)
    is_complete = models.BooleanField(verbose_name=_('is complete'), default=False)
    pay_at = models.DateField(verbose_name=_('pay at'), null=True, blank=True)
    last_reminder_sent = models.DateField(null=True, blank=True, verbose_name=_('last reminder sent'))

    class Meta:
        verbose_name = _('Installment')
        verbose_name_plural = _('Installments')

    def __str__(self):
        return f'{self.insurance} {self.amount} {self.start_at} {self.end_at}'

    @classmethod
    def unpaid_installments(cls):
        now = datetime.date.today()
        installments = cls.objects.filter(start_at__lte=now + datetime.timedelta(days=7), is_complete=False)

        return installments

    @classmethod
    def set_installments(cls, insurance, payment, installment_count, start_at):
        start_time = Insurance.convert_date(start_at)
        if payment == 'full':
            cls.objects.create(insurance=insurance, amount=insurance.amount, start_at=start_time,
                               end_at = start_time, is_complete=True, pay_at=datetime.date.today())
            return

        if insurance.insurance_type == insurance.THIRD_PARTY:
            prepayment = insurance.amount * 0.5

        elif insurance.insurance_type == insurance.COMPREHENSIVE or insurance.insurance_type == insurance.LIABILITY:
            prepayment = insurance.amount * 0.3

        elif insurance.insurance_type == insurance.FIRE:
            prepayment = insurance.amount * 0.25

        else:
            prepayment = insurance.amount

        remain = insurance.amount - prepayment
        installment_amount, remaining = round_to_nearest(remain // installment_count)
        prepayment = prepayment + (remaining * installment_count)

        instance = cls.objects.create(insurance=insurance, amount=prepayment,
                                      start_at=start_time, end_at=start_time,
                                      pay_at=datetime.date.today(), is_complete=True)
        Balance.objects.create(user=insurance.insured.owner, amount=prepayment,
                               balance_type=Balance.DEPOSIT)
        Balance.objects.create(user=insurance.insured.owner, amount=prepayment,
                               balance_type=Balance.WITHDRAW)
        Transaction.objects.create(installment=instance, amount=prepayment, is_paid=True)
        prev = instance

        for i in range(installment_count):
            prev = cls.objects.create(insurance=insurance, amount=installment_amount,
                                      start_at=prev.start_at + datetime.timedelta(days=30),
                                      end_at=prev.start_at + datetime.timedelta(days=60))


class Transaction(models.Model):
    invoice_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name=_('invoice number'))
    installment = models.OneToOneField(Installment, on_delete=models.CASCADE, related_name='transaction', verbose_name=_('installment'))
    amount = models.PositiveBigIntegerField(verbose_name=_('amount'), null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    is_paid = models.BooleanField(default=False, verbose_name=_('is paid'))

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return f'{self.invoice_number}'




class Balance(models.Model):
    DEPOSIT = 1
    WITHDRAW = 2

    choices = (
        (DEPOSIT, 'واریز'),
        (WITHDRAW, 'برداشت'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='balances', verbose_name=_('user'))
    balance_type = models.PositiveSmallIntegerField(choices=choices, verbose_name=_('type'), default=DEPOSIT)
    amount = models.PositiveBigIntegerField(verbose_name=_('amount'), null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def __str__(self):
        return f'{self.user} {self.get_balance_type_display()} {self.amount}'

    class Meta:
        verbose_name = _('Balance')
        verbose_name_plural = _('Balances')
