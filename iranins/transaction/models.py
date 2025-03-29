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

    class Meta:
        verbose_name = _('Installment')
        verbose_name_plural = _('Installments')

    def __str__(self):
        return f'{self.insurance} {self.amount} {self.start_at} {self.end_at}'


class Transaction(models.Model):
    POS = 1
    CARD = 2

    choices = (
        (POS, _('کارتخوان')),
        (CARD, _('کارت به کارت')),
    )

    invoice_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name=_('invoice number'))
    installment = models.OneToOneField(Installment, on_delete=models.CASCADE, related_name='transaction', verbose_name=_('installment'))
    payment_type = models.PositiveSmallIntegerField(choices=choices, verbose_name=_('payment type'))
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

