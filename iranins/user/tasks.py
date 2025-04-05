from celery import shared_task
from django.conf import settings
import datetime
from melipayamak import Api

from transaction.models import Installment


@shared_task
def send_sms(phone, message):
    api = Api(settings.SMS_BROKER['settings']['username'], settings.SMS_BROKER['settings']['password'])
    sms = api.sms()
    response = sms.send(phone, settings.SMS_BROKER['settings']['number'], message)


@shared_task
def get_last_installments():
    installments = Installment.objects.filter(is_complete=False, start_at__gte=datetime.date.today() + datetime.timedelta(days=7))
    for installment in installments:
        last_remind = installment.last_reminder_sent
        if last_remind and (last_remind - datetime.date.today()).days < 7:
            installment.last_reminder_sent = datetime.date.today()
            message = f'یادآوری سررسید قسط {installment.insurance.get_insurance_type_display} {installment.insurance.insured.category} {installment.insurance.insured} در تاریخ {installment.start_at}، لطفا در اسرع وقت نسبت به پرداخت آن اقدام کنید.\n بیمه ایران نمایندگی حجله - شماره کارت: {6219-8619-1811-1302}'
            send_sms.delay(installment.insurance.insured.owner.phone, message)
