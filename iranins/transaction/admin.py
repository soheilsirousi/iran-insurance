from django.contrib import admin
from transaction.models import Transaction, Installment, Balance


@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('insurance', 'amount', 'start_at', 'end_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'installment', 'amount', 'is_paid')


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance_type', 'amount', 'created_at')

