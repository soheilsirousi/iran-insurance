from django.contrib import admin
from transaction.models import Transaction, Installment


@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('insurance', 'amount', 'start_at', 'end_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'installment', 'payment_type', 'amount', 'is_paid')
