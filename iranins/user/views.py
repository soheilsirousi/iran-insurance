import datetime
from idlelib.pyparse import trans

from django.contrib.auth import login
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from transaction.models import Transaction
from user.models import CustomUser
from user.utils.otp import generate_otp, verify_otp
from user.utils.regex import check_phone


class UserLogin(View):
    template_name = 'user/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile-dashboard')

        return render(request, self.template_name)


class SendOTP(View):
    template_name = 'user/otp.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile-dashboard')

        phone = request.POST.get("phone")
        if check_phone(phone) is None:
            return HttpResponse("Invalid phone pattern.")
        code = generate_otp(phone)
        print(code)
        return render(request, self.template_name, context={'phone': phone})


class VerifyOTP(View):

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile-dashboard')

        otp = request.POST.get("otp")
        phone = request.POST.get("phone")
        if verify_otp(phone, otp):
            user = CustomUser.objects.filter(phone=phone)
            if user.exists():
                user = user.first()
                login(request, user)
            else:
                password = CustomUser.objects.make_random_password()
                user = CustomUser.objects.create_user(phone, password)
                login(request, user)
            return redirect('profile-dashboard')

        return HttpResponse("OTP Not Verified")


class ProfileDashboard(View):
    template_name = 'user/profile.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user-login')

        now = datetime.date.today()
        transactions = Transaction.objects.filter(created_at__gte=now, is_paid=True)
        total_amount = 0
        for transaction in transactions:
            total_amount += transaction.amount

        count = transactions.count()

        return render(request, self.template_name, context={'count': count, 'transactions': transactions, 'total_amount': f'{total_amount:,}'})
