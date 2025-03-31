from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from unicodedata import category

from insurance.models import Category, Insured, Attribute, InsuredAttributeValue
from transaction.models import Transaction
from user.models import CustomUser
from user.utils.decorator import admin_only
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

        status, log = CustomUser.login_user(request, phone, otp)
        if status:
            return redirect('profile-dashboard')

        messages.error(request, log)
        return redirect('user-login')


class ProfileDashboard(LoginRequiredMixin, View):
    template_name = 'user/profile.html'

    def get(self, request, *args, **kwargs):
        transactions = Transaction.get_today_transactions()
        total_amount = 0
        for transaction in transactions:
            total_amount += transaction.amount

        count = transactions.count()
        data = {'count': count, 'transactions': transactions, 'total_amount': f'{total_amount:,}'}
        return render(request, self.template_name, context=data)


class ProfileEdit(LoginRequiredMixin, View):
    template_name = 'user/profile_edit.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user-login')

        return render(request, 'user/profile_edit.html')

    def post(self, request, *args, **kwargs):
        CustomUser.edit_user(request.user, request.POST, request.FILES)

        return redirect('profile-edit')


class ProfileUsers(LoginRequiredMixin, View):
    template_name = 'user/profile_users.html'

    def get(self, request, *args, **kwargs):
        key = request.GET.get('key')
        if key is None:
            users = CustomUser.objects.all().order_by('date_joined')
        else:
            users = CustomUser.objects.filter(Q(first_name__icontains=key) | Q(last_name__icontains=key)
                                              | Q(national_id__icontains=key) | Q(phone__icontains=key)).order_by(
                'date_joined')

        paginator = Paginator(users, 40)
        page = request.GET.get('page')
        user_page = paginator.get_page(page)

        return render(request, self.template_name, context={'users': user_page})


class ProfileCreateUser(LoginRequiredMixin, View):
    template_name = 'user/profile_create_user.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        CustomUser.create_user(request.POST, request.FILES)

        return redirect('profile-users')


class ProfileUserRetreive(LoginRequiredMixin, View):
    template_name = 'user/profile_edit.html'

    def get(self, request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        if (request.user.role == 2 and user.role in [1, 2]) and (request.user != user):
            messages.error(request, 'پشتیبان نمیتواند کاربر مدیر یا پشتیبان را ویرایش کند.')
            return redirect('profile-users')

        return render(request, self.template_name, context={'user': user})

    def post(self, request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        if request.user.role == 2 and user.role in [1, 2] and (request.user != user):
            messages.error(request, 'پشتیبان نمیتواند کاربر مدیر یا پشتیبان را ویرایش کند.')
            return redirect('profile-users')

        CustomUser.edit_user(user, request.POST, request.FILES)

        return redirect('profile-users')


class ProfileUserDelete(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        if request.user.role == 2 and user.role in [1, 2]:
            messages.error(request, 'پشتیبان نمیتواند کاربر مدیر یا پشتیبان را حذف کند.')
            return redirect('profile-users')
        elif request.user == user:
            messages.error(request, "نمیتوانید خودتان را حذف کنید.")
            return redirect('profile-users')

        user.delete()
        return redirect('profile-users')


class UserInsureds(LoginRequiredMixin, View):
    template_name = 'user/user_insureds.html'

    def get(self, request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        key = request.GET.get('key')
        categories = Category.objects.all()

        if key is None:
            insureds = user.insureds.all().order_by('joined_at')
        else:
            insureds = user.insureds.filter(Q(name__icontains=key) | Q(category__name__icontains=key)).order_by(
                'joined_at')

        paginator = Paginator(insureds, 10)
        page = request.GET.get('page')
        insureds_page = paginator.get_page(page)

        return render(request, self.template_name,
                      context={'user': user, 'insureds': insureds_page, 'categories': categories})


class UserInsuredDelete(LoginRequiredMixin, View):

    def get(self, request, user_pk, insured_pk, *args, **kwargs):
        if request.user.role == 2:
            messages.error(request, 'پشتیبان نمیتواند دارایی را حذف کند.')
            return redirect('user-insureds', pk=user_pk)

        user = CustomUser.objects.get(pk=user_pk)
        insured = user.insureds.get(pk=insured_pk)

        insured.delete()

        return redirect('user-insureds', pk=user_pk)


class UserInsuredAdd(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        name = request.POST.get('name')
        type = request.POST.get('type')
        user = CustomUser.objects.get(pk=pk)
        category = Category.objects.get(pk=int(type))
        insured = Insured.objects.create(owner=user, name=name, category=category)

        attrs = request.POST.items()
        attribute = None
        for title, name in attrs:
            if title.startswith('property-title-'):
                try:
                    attribute = Attribute.objects.get(name=name)
                except Attribute.DoesNotExist:
                    attribute = Attribute.objects.create(name=name)

            elif title.startswith('property-value-'):
                InsuredAttributeValue.objects.create(attribute=attribute, value=name, insured=insured)

        return redirect('user-insureds', pk=pk)


class UserInsuredEdit(LoginRequiredMixin, View):
    template_name = 'user/user_insured_edit.html'

    def get(self, request, user_pk, insured_pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=user_pk)
        insured = user.insureds.get(pk=insured_pk)
        categories = Category.objects.all()
        return render(request, self.template_name, context={'user': user, 'insured': insured, 'categories': categories})

    def post(self, request, user_pk, insured_pk, *args, **kwargs):
        name = request.POST.get('name')
        type = request.POST.get('type')
        user = CustomUser.objects.get(pk=user_pk)
        insured = Insured.objects.get(pk=int(insured_pk))

        insured.name = name
        insured.category = Category.objects.get(pk=int(type))
        insured.save()

        for obj in insured.attributes.all():
            obj.delete()

        attrs = request.POST.items()
        attribute = None
        for title, name in attrs:
            if title.startswith('attribute_names'):
                try:
                    attribute = Attribute.objects.get(name=name)
                except Attribute.DoesNotExist:
                    attribute = Attribute.objects.create(name=name)

            elif title.startswith('attribute_values'):
                InsuredAttributeValue.objects.create(attribute=attribute, value=name, insured=insured)

        return redirect('user-insureds', pk=user_pk)


class InsuredInsurance(LoginRequiredMixin, View):
    template_name = 'user/insured_insurances.html'

    def get(self, request, user_pk, insured_pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=user_pk)
        insured = user.insureds.get(pk=insured_pk)
        insurances = insured.insurances.all()

        return render(request, self.template_name, context={'user': user, 'insured': insured, 'insurances': insurances})


class InsuredInsuranceAdd(LoginRequiredMixin, View):

    def post(self, request, user_pk, insured_pk, *args, **kwargs):
        print(request.POST)


class ErrorPage(View):
    template_name = 'user/error.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ProfileLogout(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        login_required()
        logout(request)
        return redirect('user-login')
