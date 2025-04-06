from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from transaction.models import Installment
from user.models import CustomUser


class ChargeBalance(LoginRequiredMixin, View):
    template_name = 'transaction/charge_balance.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UserTransactions(LoginRequiredMixin, View):
    template_name = 'transaction/user_transactions.html'

    def get(self, request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        installments = Installment.objects.filter(insurance__insured__owner=user, is_complete=True).order_by('pay_at')
        return render(request, self.template_name, {'installments': installments, 'user': user})
