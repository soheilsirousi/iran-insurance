from celery import shared_task
from django.conf import settings
import datetime
from melipayamak import Api
import jdatetime
from transaction.models import Installment, Transaction, Balance
from user.models import CustomUser


@shared_task
def send_sms(phone, message):
    api = Api(settings.SMS_BROKER['settings']['username'], settings.SMS_BROKER['settings']['password'])
    sms = api.sms()
    response = sms.send(phone, settings.SMS_BROKER['settings']['number'], message)


@shared_task
def remind_installments():
    installments = Installment.objects.filter(is_complete=False, start_at__lte=datetime.date.today() + datetime.timedelta(days=7))
    for installment in installments:
        user = installment.insurance.insured.owner
        if user.on_block_list:
            continue
        last_remind = installment.last_reminder_sent
        if user.get_balance() >= installment.amount:
            installment.is_complete = True
            installment.save()
            Balance.objects.create(user=user, amount=installment.amount, balance_type=Balance.WITHDRAW)
            continue
        if datetime.date.today() > installment.end_at:
            date = jdatetime.date.fromgregorian(date=installment.end_at).strftime("%Y/%m/%d")
            message = 'قسط بیمه {} {} {} مشتری {} از موعد پرداخت ({}) گذشته و پرداخت نشده است.\n مبلغ پرداخت: {} تومان'.format(
                installment.insurance.get_insurance_type_display(),
                installment.insurance.insured.category,
                installment.insurance.insured,
                user.get_full_name(),
                date,
                installment.amount
            )
            for manager in CustomUser.objects.filter(role=CustomUser.OWNER):
                send_sms.delay(manager.phone, message)

        else:
            if (last_remind and (last_remind - datetime.date.today()).days >= 7) or last_remind is None:
                installment.last_reminder_sent = datetime.date.today()
                date = jdatetime.date.fromgregorian(date=installment.start_at).strftime("%Y/%m/%d")
                message = 'با سلام آقا/خانم {}\n سررسید قسط بیمه {} {} {} مورخ:\n {} \n مبلغ: {:,} تومان \n شماره کارت: {}\n بنام سید اسماعیل حجله\n با تشکر بیمه ایران'.format(
                    user.get_full_name(), installment.insurance.get_insurance_type_display(),
                    installment.insurance.insured.category, installment.insurance.insured, date,
                    installment.amount, '6104337878433281')
                send_sms.delay(user.phone, message)
