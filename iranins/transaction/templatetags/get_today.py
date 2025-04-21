import datetime
from django import template
import jdatetime


register = template.Library()

@register.simple_tag()
def get_today():
    today = datetime.date.today()
    return jdatetime.date.fromgregorian(date=today).strftime("%Y/%m/%d")
