from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
import datetime
from django.views import View

from insurance.models import Insurance
from log.models import Log
from transaction.models import Installment, Balance
from user.models import CustomUser


class ChargeBalance(LoginRequiredMixin, View):
    template_name = 'transaction/charge_balance.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        date = Insurance.convert_date(request.POST.get('date'))
        if phone is None or amount is None or date is None:
            messages.error(request, "شماره همراه و مبلغ و تاریخ الزامی می باشد.")
            return redirect('charge-balance')

        user = CustomUser.objects.filter(phone=phone)
        if not user.exists():
            messages.error(request, "کاربر یافت نشد.")
            return redirect('charge-balance')

        if int(amount) <= 0:
            messages.error(request, 'مبلغ شارژ نمیتواند منفی یا صفر باشد.')
            return redirect('charge-balance')

        instance = Balance.objects.create(user=user.first(), amount=int(amount))
        instance.created_at = datetime.datetime(year=date.year, month=date.month, day=date.day)
        instance.save()
        messages.success(request, "شارژ حساب با موفقیت انجام شد.")

        Log.create_log(request.user, instance.user, Log.CREATE, instance)
        return redirect('charge-balance')


class UserTransactions(LoginRequiredMixin, View):
    template_name = 'transaction/user_transactions.html'

    def get(self, request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        installments = Installment.objects.filter(insurance__insured__owner=user, is_complete=True).order_by('pay_at')

        paginator = Paginator(installments, 20)
        page = request.GET.get('page')
        installments = paginator.get_page(page)

        return render(request, self.template_name, {'installments': installments, 'user': user})
