from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from insurance.models import Insurance
from user.tasks import send_sms
import jdatetime


class MainPage(View):

    def get(self, request, *args, **kwargs):
        return redirect('unpaid-installments')


class InsuranceReminder(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        insurance = Insurance.objects.get(pk=pk)
        date = jdatetime.date.fromgregorian(date=insurance.end_at).strftime("%Y/%m/%d")
        message = 'با سلام آقا/خانم {}\n بیمه {} {} {} در تاریخ {} به پایان می رسد.\n با تشکر بیمه ایران'.format(
            insurance.insured.owner.get_full_name(),
            insurance.get_insurance_type_display(),
            insurance.insured.category,
            insurance.insured.name,
            date
        )
        send_sms.delay(insurance.insured.owner.phone, message)
        return redirect('expired-insurances')
