import datetime
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from insurance.models import Insurance


class Installment(models.Model):
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name='installments', verbose_name=_('installment'))
    amount = models.PositiveBigIntegerField(verbose_name=_('amount'), null=False, blank=False)
    start_at = models.DateField(verbose_name=_('start at'), null=False, blank=False)
    end_at = models.DateField(verbose_name=_('end at'), null=False, blank=False)
    is_complete = models.BooleanField(verbose_name=_('is complete'), default=False)
    last_reminder_sent = models.DateField(null=True, blank=True, verbose_name=_('last reminder sent'))

    class Meta:
        verbose_name = _('Installment')
        verbose_name_plural = _('Installments')

    def __str__(self):
        return f'{self.insurance} {self.amount} {self.start_at} {self.end_at}'

    @classmethod
    def set_installments(cls, insurance, payment, installment_count):
        if payment == 'full':
            cls.objects.create(insurance=insurance, amount=insurance.amount, start_at=datetime.date.today(),
                               end_at = datetime.date.today(), is_complete=True)
            return

        if insurance.insurance_type == insurance.THIRD_PARTY:
            prepayment = insurance.amount * 0.5

        elif insurance.insurance_type == insurance.COMPREHENSIVE or insurance.insurance_type == insurance.LIABILITY:
            prepayment = insurance.amount * 0.3

        elif insurance.insurance_type == insurance.FIRE:
            prepayment = insurance.amount * 0.25

        else:
            prepayment = insurance.amount

        instance = cls.objects.create(insurance=insurance, amount=prepayment,
                                      start_at=datetime.date.today(), end_at=datetime.date.today(),
                                      is_complete=True)
        Transaction.objects.create(installment=instance, amount=prepayment, is_paid=True)
        prev = instance
        remain = insurance.amount - prepayment
        for i in range(installment_count):
            prev = cls.objects.create(insurance=insurance, amount=remain // installment_count,
                                      start_at=prev.start_at + datetime.timedelta(days=30),
                                      end_at=prev.start_at + datetime.timedelta(days=60))


class Transaction(models.Model):
    POS = 1
    CARD = 2

    choices = (
        (POS, _('کارتخوان')),
        (CARD, _('کارت به کارت')),
    )

    invoice_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name=_('invoice number'))
    installment = models.OneToOneField(Installment, on_delete=models.CASCADE, related_name='transaction', verbose_name=_('installment'))
    payment_type = models.PositiveSmallIntegerField(choices=choices, verbose_name=_('payment type'), default=CARD)
    amount = models.PositiveBigIntegerField(verbose_name=_('amount'), null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    is_paid = models.BooleanField(default=False, verbose_name=_('is paid'))

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return f'{self.invoice_number}'

    @classmethod
    def get_today_transactions(cls):
        now = datetime.date.today()
        transactions = Transaction.objects.filter(created_at__gte=now, is_paid=True)

        return transactions

